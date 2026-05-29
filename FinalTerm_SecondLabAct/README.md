# Distributed Voting System

A demonstration of distributed systems concepts using **Supabase (PostgreSQL)**,
**Flask**, and Python's **in-process Queue** — built as a final laboratory
requirement for a Computer Science course.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Folder Structure](#folder-structure)
4. [Prerequisites](#prerequisites)
5. [Supabase Setup](#supabase-setup)
6. [Local Setup](#local-setup)
7. [Running the System](#running-the-system)
8. [Fault Injection Tests](#fault-injection-tests)
9. [Observations and Analysis](#observations-and-analysis)
10. [Distributed Systems Concepts Demonstrated](#distributed-systems-concepts-demonstrated)
11. [Reflection](#reflection)

---

## System Overview

This project simulates a real-world distributed voting platform where:

* **Multiple edge nodes** (distributed clients) generate ballots independently
  and forward them to a central API over HTTP.
* The **Flask API** validates each ballot and drops it into an in-memory
  **Python Queue**, decoupling ingestion from persistence.
* A **Worker process** drains the queue and writes to **Supabase (PostgreSQL)**
  using an *upsert* — ensuring exactly-once persistence regardless of duplicate
  network deliveries.
* End-to-end **latency** is measured from the moment the edge node stamps the
  ballot to the moment the worker commits it to the database.

The architecture deliberately mirrors production patterns (Kafka → consumer →
database) at a scale that runs on a single laptop.

---

## Architecture Diagram

```
  ┌──────────────────────────────────────────────────────────────┐
  │                     DISTRIBUTED EDGE LAYER                   │
  │                                                              │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
  │  │   edge-1    │  │   edge-2    │  │   edge-3    │  ...     │
  │  │  (Python)   │  │  (Python)   │  │  (Python)   │         │
  │  │             │  │             │  │             │         │
  │  │ • Random    │  │ • Random    │  │ • Random    │         │
  │  │   votes     │  │   votes     │  │   votes     │         │
  │  │ • Retry ×3  │  │ • Retry ×3  │  │ • Retry ×3  │         │
  │  │ • Dup test  │  │             │  │             │         │
  └──┴──────┬──────┴──┴──────┬──────┴──┴──────┬──────┴─────────┘
            │   POST /vote   │                │
            └────────────────┼────────────────┘
                             │  HTTP (JSON)
                             ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                       API LAYER (Flask)                      │
  │                                                              │
  │   POST /vote                                                 │
  │   ├── Validate payload                                       │
  │   ├── queue.put(vote)          ← thread-safe enqueue         │
  │   └── return { status, queue_size, vote_id }                 │
  │                                                              │
  │   GET  /health   GET /queue/size                             │
  └──────────────────────────────┬───────────────────────────────┘
                                 │  Shared in-memory Queue
                                 │  (stdlib queue.Queue)
                                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                    MESSAGE QUEUE LAYER                       │
  │                                                              │
  │   queue.Queue(maxsize=0)  ← unbounded; grows during outage   │
  │                                                              │
  │   [ vote_A | vote_B | vote_C | vote_D | ... ]               │
  │     ↑                                   ↑                    │
  │   oldest                             newest                  │
  └──────────────────────────────┬───────────────────────────────┘
                                 │  queue.get()
                                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                      WORKER LAYER (Python)                   │
  │                                                              │
  │   while True:                                                │
  │       if not worker_enabled: sleep(); continue  ← fault sim  │
  │       vote = queue.get()                                     │
  │       supabase.upsert(vote, on_conflict="id")  ← idempotent  │
  │       print latency = now() − vote.timestamp                 │
  │                                                              │
  │   Control server  →  http://127.0.0.1:5001                   │
  │   SIGUSR1 toggle  →  kill -USR1 <pid>                        │
  └──────────────────────────────┬───────────────────────────────┘
                                 │  supabase-py upsert
                                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │              DATABASE LAYER (Supabase / PostgreSQL)          │
  │                                                              │
  │   Table: votes                                               │
  │   ┌─────────────────┬──────────┬──────────┬──────────┐      │
  │   │       id        │ user_id  │ poll_id  │  choice  │ ...  │
  │   ├─────────────────┼──────────┼──────────┼──────────┤      │
  │   │ user_001_poll_m │ user_001 │poll_mayor│  Alice   │      │
  │   │ user_002_poll_s │ user_002 │poll_sen. │  Dave    │      │
  │   └─────────────────┴──────────┴──────────┴──────────┘      │
  │   PRIMARY KEY = id  (user_id + "_" + poll_id)                │
  │   Upsert → duplicate network messages = zero duplicate rows  │
  └──────────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
distributed-voting-system/
│
├── edge/
│   └── edge_node.py        # Distributed client – generates & sends votes
│
├── api/
│   └── app.py              # Flask API – validates & enqueues votes
│
├── worker/
│   └── worker.py           # Worker – drains queue, upserts to Supabase
│
├── shared/
│   ├── __init__.py
│   └── queue_manager.py    # Singleton queue shared by API & Worker
│
├── run.py                  # Convenience launcher (API + Worker together)
├── supabase_schema.sql     # SQL to create the votes table
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10 or higher |
| pip | 23+ |
| Supabase account | Free tier is fine |

---

## Supabase Setup

1. Create a free project at [supabase.com](https://supabase.com).
2. In the Supabase dashboard go to **SQL Editor**.
3. Paste the contents of `supabase_schema.sql` and click **Run**.
4. Go to **Settings → API** and copy:
   * **Project URL** → `SUPABASE_URL`
   * **anon / public key** → `SUPABASE_KEY`

---

## Local Setup

```bash
# 1. Clone / enter the project
cd distributed-voting-system

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and fill in SUPABASE_URL and SUPABASE_KEY
```

---

## Running the System

### Option A — All-in-one (recommended for quick demo)

```bash
python run.py
```

This starts the Flask API (port 5000) and the Worker in the same process,
sharing the in-memory queue automatically.

---

### Option B — Three separate terminals

**Terminal 1 – API**
```bash
python api/app.py
```

**Terminal 2 – Worker**
```bash
python worker/worker.py
```

**Terminal 3 – Edge node(s)**
```bash
# Single edge node
python edge/edge_node.py --edge-id edge-1

# Second edge node (new terminal, different ID)
python edge/edge_node.py --edge-id edge-2

# Edge node with duplicate sending enabled (idempotency test)
python edge/edge_node.py --edge-id edge-3 --duplicates --duplicate-rate 0.3
```

---

### Verifying the API manually

```bash
# Health check
curl http://127.0.0.1:5000/health

# Submit a vote manually
curl -X POST http://127.0.0.1:5000/vote \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_001","poll_id":"poll_mayor","choice":"Alice","edge_id":"manual","timestamp":'"$(python -c 'import time; print(time.time())')"'}'

# Check queue depth
curl http://127.0.0.1:5000/queue/size
```

---

## Fault Injection Tests

### Test 1 — Idempotency (duplicate messages)

**Goal:** Prove that sending the same (user_id, poll_id) twice does not create
duplicate rows in the database.

```bash
# Start everything normally, then run an edge node with duplicates enabled
python edge/edge_node.py --edge-id edge-dup --duplicates --duplicate-rate 0.5
```

**Expected observations:**
* The edge node logs `↩ Sending DUPLICATE` for ~50 % of messages.
* The worker logs `✓ Persisted` for each message (upsert succeeds silently).
* In Supabase → Table Editor, the `votes` table has **no duplicate rows** —
  the `id` count matches the number of unique (user, poll) pairs, not the
  total messages sent.

---

### Test 2 — Worker failure & queue buildup

**Goal:** Disable the worker and observe the queue growing.  Re-enable it and
observe the backlog being drained (eventual consistency).

**Step 1 – Disable the worker via HTTP:**
```bash
curl -X POST http://127.0.0.1:5001/disable
```

**Step 2 – Watch the queue grow:**
```bash
# Poll the queue size while edge nodes keep sending
watch -n 1 'curl -s http://127.0.0.1:5000/queue/size'
```

**Step 3 – Confirm nothing is written to Supabase** (open Table Editor and
refresh a few times — the row count should be frozen).

**Step 4 – Re-enable the worker:**
```bash
curl -X POST http://127.0.0.1:5001/enable
```

**Step 5 – Observe recovery:**
* Worker terminal floods with `✓ Persisted` lines.
* Queue size in `/queue/size` drops toward zero.
* Supabase row count catches up to the unique-vote count.
* Latency values reported by the worker will be **much higher** than normal
  because the votes were queued while the worker was paused.

**On Linux/macOS you can also use a signal:**
```bash
# Get the worker PID
ps aux | grep worker.py
# Toggle with SIGUSR1
kill -USR1 <pid>
```

---

### Test 3 — Edge node retry logic

**Goal:** Prove the retry mechanism handles temporary API unavailability.

```bash
# 1. Stop the API (Ctrl+C in its terminal or kill the process)
# 2. Start an edge node
python edge/edge_node.py --edge-id edge-retry
# 3. Observe retry logs: "✗ Connection refused on attempt 1/3"
# 4. Restart the API
python api/app.py
# 5. Observe the edge node succeed on the next cycle
```

---

### Test 4 — Multiple concurrent edge nodes

**Goal:** Show that several distributed clients can write concurrently without
race conditions.

```bash
# Open 4 terminals simultaneously:
python edge/edge_node.py --edge-id edge-1
python edge/edge_node.py --edge-id edge-2
python edge/edge_node.py --edge-id edge-3
python edge/edge_node.py --edge-id edge-4
```

Watch the worker terminal interleave votes from all four edge IDs. The queue
depth may briefly spike but the worker will keep up.

---

## Observations and Analysis

### Latency

Under normal operation, **end-to-end latency** (edge timestamp → worker commit)
is typically **50–300 ms**, dominated by:
1. Network round-trip to the Supabase cloud (~40–150 ms depending on region).
2. Flask overhead (<1 ms).
3. Queue serialisation (<0.1 ms, in-memory).

During worker-disabled periods the queue accumulates, and when the worker
resumes, latency for the first items off the queue reflects the *total pause
duration* — sometimes tens of seconds.

### Queue as a buffer

The Python Queue acts as a **durable buffer** (within the process lifetime),
absorbing spikes in incoming vote rate and smoothing them out for the database.
This is the same role Kafka or RabbitMQ plays in production systems.

### Idempotency

The upsert approach on `id = user_id + "_" + poll_id` guarantees that at-most-
once semantics are enforced at the database level regardless of how many times
an edge node retransmits a vote. This is critical in distributed systems where
"exactly-once" delivery is impossible at the network layer.

### Eventual Consistency

While the worker is paused, the system is **temporarily inconsistent** — the
in-memory queue holds truth that has not yet been persisted. Once the worker
resumes, the system *eventually converges* to a consistent state. This models
BASE (Basically Available, Soft-state, Eventually consistent) behaviour.

---

## Distributed Systems Concepts Demonstrated

| Concept | Where in this project |
|---|---|
| **Distributed clients** | Multiple `edge_node.py` instances with unique IDs |
| **Asynchronous processing** | Flask enqueues; Worker processes independently |
| **Message queue / buffering** | `queue.Queue` decouples producers from consumers |
| **Idempotency** | Upsert on `id` PK prevents duplicate rows |
| **Retry logic** | Edge node retries 3× with back-off on HTTP failure |
| **Fault tolerance** | Queue persists during worker downtime |
| **Worker recovery** | Re-enabling worker drains the backlog automatically |
| **Eventual consistency** | System converges after transient worker failure |
| **Latency measurement** | Worker computes `now() − vote.timestamp` per item |
| **Fault injection** | HTTP control endpoint + SIGUSR1 signal |

---

## Reflection

### 1. Sequential vs. Distributed Execution
If we had built this normally (sequentially), the system would have to stop and wait for the database to finish saving every single time someone voted. If the database was being slow, the whole app would freeze. 

By building it as a distributed system, we completely separated the pieces. Our edge nodes just rapidly fire off votes to the Flask API and move on. The API grabs the vote, tosses it into a Python queue, and instantly tells the user "success!" Meanwhile, a completely separate background worker pulls votes from that queue and saves them to Supabase. This means the edge nodes never have to wait around for the database.

### 2. System Performance & Load
When we opened up four different terminals to run multiple edge nodes at the same time, the system handled the load perfectly. 

To really test it, we purposely "crashed" the worker. Instead of crashing the whole API or losing votes, the votes just safely piled up in the Python queue (acting like a Pub/Sub buffer). The API stayed lightning fast, but the *end-to-end latency* (the total time it took for a vote to actually reach the database) spiked because the votes were stuck waiting in line.

### 3. Challenges and Debugging
Honestly, the hardest part was debugging. Having four terminal windows open at the same time made it confusing to figure out where an error was coming from! 

Some specific issues we ran into:
* **Database Security:** When we first connected to Supabase, our worker kept failing. It turned out Supabase has Row-Level Security (RLS) turned on by default, which blocked our script from inserting any data until we turned it off. We also accidentally broke our `.env` API key at one point.
* **Threading Errors:** We got a weird `ValueError` because we tried to set up a system signal to pause the worker, but Python doesn't let you do that inside a background thread. We had to rewrite the code to catch and ignore that error.

### 4. Buffering and Eventual Consistency
The queue was the absolute backbone of this project. When we paused the worker during the test, a user's vote was technically "received" by the API, but if you looked in the Supabase database, it wasn't there yet. The system was temporarily out of sync. 

This taught us about **eventual consistency**. Once we turned the worker back on, it rapidly drained the queue and the database finally caught up. 

We also learned about **idempotency**. Because our edge nodes were programmed to retry if the connection failed, they sometimes sent the same vote twice. To prevent double-counting, we had to use an "upsert" in Supabase with a combined primary key (`user_id` + `poll_id`), ensuring the database only accepted one vote per person.

### 5. Was it worth it? (Pros and Cons)
**The Good:** The resilience is amazing. If our database completely crashes for 5 minutes, a normal app would go down with it. In our distributed app, people can keep voting seamlessly and the API will just hold the votes in the queue until the database comes back online.

**The Bad:** It is so much more complicated. For a simple voting app, this is massive overkill. We had to write separate scripts for the API, the worker, and the edge nodes, worry about thread safety, handle HTTP retries, and set up database constraints to prevent duplicate data. It's a lot harder to build and debug than a simple, single-file script.

---

*Lab requirement — Computer Science, Distributed Systems*  
*Stack: Python 3.10+, Flask, supabase-py, python-dotenv*
