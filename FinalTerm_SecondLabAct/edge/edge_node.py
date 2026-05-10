"""
edge_node.py
------------
Simulates a distributed edge node that generates random votes and sends
them to the central Flask API. Supports retry logic and duplicate sending
for idempotency testing.

Run multiple instances with different EDGE_ID values to simulate a
distributed environment.
"""

import os
import time
import random
import argparse
import requests
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

API_URL       = os.getenv("API_URL", "http://127.0.0.1:5000")
EDGE_ID       = os.getenv("EDGE_ID", "edge-1")       # Override per instance
MAX_RETRIES   = 3                                      # Retry attempts per vote
RETRY_DELAY   = 1.5                                    # Seconds between retries
MIN_INTERVAL  = 1.0                                    # Min seconds between votes
MAX_INTERVAL  = 3.0                                    # Max seconds between votes

# Sample data pools
USER_IDS  = [f"user_{i:03d}" for i in range(1, 21)]   # user_001 … user_020
POLL_IDS  = ["poll_mayor", "poll_senator", "poll_governor"]
CHOICES   = {
    "poll_mayor":    ["Alice", "Bob", "Carol"],
    "poll_senator":  ["Dave", "Eve", "Frank"],
    "poll_governor": ["Grace", "Hank", "Iris"],
}


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def build_vote(user_id: str, poll_id: str, send_duplicate: bool = False) -> dict:
    """
    Construct a vote payload.

    The (user_id, poll_id) pair is the idempotency key on the server side.
    Sending the same pair twice is what tests duplicate-rejection.
    """
    return {
        "user_id":   user_id,
        "poll_id":   poll_id,
        "choice":    random.choice(CHOICES[poll_id]),
        "edge_id":   EDGE_ID,
        "timestamp": time.time(),   # Used by the worker to compute latency
    }


def send_vote(payload: dict, attempt: int = 1) -> bool:
    """
    POST a single vote to the API with retry logic.

    Returns True on success, False after all retries are exhausted.
    """
    url = f"{API_URL}/vote"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(
                    f"[{EDGE_ID}] ✓ Vote sent  | "
                    f"user={payload['user_id']} poll={payload['poll_id']} "
                    f"choice={payload['choice']} | "
                    f"queue_size={data.get('queue_size', '?')}"
                )
                return True
            else:
                print(
                    f"[{EDGE_ID}] ✗ HTTP {response.status_code} on attempt "
                    f"{attempt}/{MAX_RETRIES}: {response.text[:120]}"
                )
        except requests.exceptions.ConnectionError:
            print(
                f"[{EDGE_ID}] ✗ Connection refused on attempt "
                f"{attempt}/{MAX_RETRIES} — is the API running?"
            )
        except requests.exceptions.Timeout:
            print(
                f"[{EDGE_ID}] ✗ Timeout on attempt {attempt}/{MAX_RETRIES}"
            )
        except Exception as exc:
            print(f"[{EDGE_ID}] ✗ Unexpected error on attempt {attempt}: {exc}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    print(f"[{EDGE_ID}] ✗ Gave up after {MAX_RETRIES} attempts.")
    return False


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run(send_duplicates: bool = False, duplicate_rate: float = 0.2):
    """
    Continuously generate and send votes.

    Args:
        send_duplicates:  If True, occasionally re-send the same (user, poll)
                          pair to test server-side idempotency.
        duplicate_rate:   Fraction of votes (0–1) that will be duplicates.
    """
    print(f"[{EDGE_ID}] Edge node starting. API={API_URL}  duplicates={send_duplicates}")
    history: list[dict] = []   # Keep recent votes to replay as duplicates

    while True:
        user_id = random.choice(USER_IDS)
        poll_id = random.choice(POLL_IDS)

        # Decide whether to replay a past vote (idempotency test)
        if send_duplicates and history and random.random() < duplicate_rate:
            past = random.choice(history)
            payload = past.copy()
            payload["timestamp"] = time.time()   # Fresh timestamp; same IDs
            print(f"[{EDGE_ID}] ↩ Sending DUPLICATE: user={past['user_id']} poll={past['poll_id']}")
        else:
            payload = build_vote(user_id, poll_id)
            history.append(payload)
            if len(history) > 50:          # Keep history bounded
                history.pop(0)

        send_vote(payload)
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed Voting Edge Node")
    parser.add_argument(
        "--edge-id",
        default=EDGE_ID,
        help="Unique identifier for this edge node (default: from .env or 'edge-1')",
    )
    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="Enable duplicate vote sending to test idempotency",
    )
    parser.add_argument(
        "--duplicate-rate",
        type=float,
        default=0.2,
        help="Fraction of votes that are duplicates when --duplicates is set (default: 0.2)",
    )
    args = parser.parse_args()

    # CLI flag overrides env var
    EDGE_ID = args.edge_id

    try:
        run(send_duplicates=args.duplicates, duplicate_rate=args.duplicate_rate)
    except KeyboardInterrupt:
        print(f"\n[{EDGE_ID}] Shutting down.")
