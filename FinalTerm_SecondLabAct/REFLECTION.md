# Distributed Systems Lab: Final Reflection

By [Your Name Here]

### 1. Sequential vs. Distributed Execution
If I had built this normally (sequentially), the system would have to stop and wait for the database to finish saving every single time someone voted. If the database was being slow, the whole app would freeze. 

By building it as a distributed system, I completely separated the pieces. My edge nodes just rapidly fire off votes to the Flask API and move on. The API grabs the vote, tosses it into a Python queue, and instantly tells the user "success!" Meanwhile, a completely separate background worker pulls votes from that queue and saves them to Supabase. This means the edge nodes never have to wait around for the database.

### 2. System Performance & Load
When I opened up four different terminals to run multiple edge nodes at the same time, the system handled the load perfectly. 

To really test it, I purposely "crashed" the worker. Instead of crashing the whole API or losing votes, the votes just safely piled up in the Python queue (acting like a Pub/Sub buffer). The API stayed lightning fast, but the *end-to-end latency* (the total time it took for a vote to actually reach the database) spiked because the votes were stuck waiting in line.

### 3. Challenges and Debugging
Honestly, the hardest part was debugging. Having four terminal windows open at the same time made it confusing to figure out where an error was coming from! 

Some specific issues I ran into:
* **Database Security:** When I first connected to Supabase, my worker kept failing. It turned out Supabase has Row-Level Security (RLS) turned on by default, which blocked my script from inserting any data until I turned it off. I also accidentally broke my `.env` API key at one point.
* **Threading Errors:** I got a weird `ValueError` because I tried to set up a system signal to pause the worker, but Python doesn't let you do that inside a background thread. I had to rewrite the code to catch and ignore that error.

### 4. Buffering and Eventual Consistency
The queue was the absolute backbone of this project. When I paused my worker during the test, a user's vote was technically "received" by the API, but if you looked in the Supabase database, it wasn't there yet. The system was temporarily out of sync. 

This taught me about **eventual consistency**. Once I turned the worker back on, it rapidly drained the queue and the database finally caught up. 

I also learned about **idempotency**. Because my edge nodes were programmed to retry if the connection failed, they sometimes sent the same vote twice. To prevent double-counting, I had to use an "upsert" in Supabase with a combined primary key (`user_id` + `poll_id`), ensuring the database only accepted one vote per person.

### 5. Was it worth it? (Pros and Cons)
**The Good:** The resilience is amazing. If my database completely crashes for 5 minutes, a normal app would go down with it. In my distributed app, people can keep voting seamlessly and the API will just hold the votes in the queue until the database comes back online.

**The Bad:** It is so much more complicated. For a simple voting app, this is massive overkill. I had to write separate scripts for the API, the worker, and the edge nodes, worry about thread safety, handle HTTP retries, and set up database constraints to prevent duplicate data. It's a lot harder to build and debug than a simple, single-file script.
