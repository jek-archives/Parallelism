import os
import sys
import time
import signal
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from supabase import create_client, Client
from shared.queue_manager import get_queue

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
TABLE_NAME:   str = os.getenv("SUPABASE_TABLE", "votes")

POLL_INTERVAL:  float = 0.5
RETRY_ATTEMPTS: int   = 3
RETRY_DELAY:    float = 2.0


worker_enabled: bool = True


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_KEY must be set in .env"
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def process_vote(client: Client, vote: dict) -> bool:
    vote_id = f"{vote['user_id']}_{vote['poll_id']}"
    record  = {
        "id":        vote_id,
        "user_id":   vote["user_id"],
        "poll_id":   vote["poll_id"],
        "choice":    vote["choice"],
        "edge_id":   vote["edge_id"],
        "timestamp": vote["timestamp"],
    }

    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            (
                client.table(TABLE_NAME)
                      .upsert(record, on_conflict="id")
                      .execute()
            )


            latency_ms = (time.time() - vote["timestamp"]) * 1000
            print(
                f"[Worker] ✓ Persisted  id={vote_id:40s} | "
                f"edge={vote['edge_id']:8s} | "
                f"latency={latency_ms:8.1f} ms"
            )
            return True

        except Exception as exc:
            print(
                f"[Worker] ✗ DB error on attempt {attempt}/{RETRY_ATTEMPTS} "
                f"for id={vote_id}: {exc}"
            )
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_DELAY)

    print(f"[Worker] ✗ Gave up persisting id={vote_id} after {RETRY_ATTEMPTS} attempts.")
    return False


def run_worker():
    global worker_enabled

    print("[Worker] Connecting to Supabase…")
    client = get_supabase_client()
    print(f"[Worker] Connected. Watching table '{TABLE_NAME}'. worker_enabled={worker_enabled}")

    queue = get_queue()

    while True:
        if not worker_enabled:
            print("[Worker] ⏸  Worker disabled — queue is accumulating…")
            time.sleep(2)
            continue

        if queue.empty():
            time.sleep(POLL_INTERVAL)
            continue

        vote = queue.get()
        process_vote(client, vote)
        queue.task_done()




def _toggle_handler(signum, frame):
    global worker_enabled
    worker_enabled = not worker_enabled
    state = "ENABLED ▶" if worker_enabled else "DISABLED ⏸"
    print(f"\n[Worker] ⚡ Fault injection: worker is now {state}\n")


try:
    signal.signal(signal.SIGUSR1, _toggle_handler)
    print("[Worker] SIGUSR1 handler registered (send SIGUSR1 to toggle worker_enabled)")
except (AttributeError, OSError, ValueError):
    print("[Worker] SIGUSR1 not available on this OS or not in main thread; use CLI/HTTP control instead.")




def _start_control_server():
    try:
        # pyrefly: ignore [missing-import]
        from flask import Flask as _Flask, jsonify as _jsonify
        ctrl = _Flask("worker_control")
        ctrl_queue = get_queue()

        @ctrl.route("/status")
        def _status():
            return _jsonify({
                "worker_enabled": worker_enabled,
                "queue_size":     ctrl_queue.qsize(),
            })

        @ctrl.route("/disable", methods=["POST"])
        def _disable():
            global worker_enabled
            worker_enabled = False
            print("[Control] Worker DISABLED via HTTP")
            return _jsonify({"worker_enabled": False})

        @ctrl.route("/enable", methods=["POST"])
        def _enable():
            global worker_enabled
            worker_enabled = True
            print("[Control] Worker ENABLED via HTTP")
            return _jsonify({"worker_enabled": True})

        import logging
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)
        ctrl.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)
    except Exception as exc:
        print(f"[Control] Could not start control server: {exc}")


ctrl_thread = threading.Thread(target=_start_control_server, daemon=True)
ctrl_thread.start()
print("[Worker] Control server started on http://127.0.0.1:5001")


if __name__ == "__main__":
    try:
        run_worker()
    except KeyboardInterrupt:
        print("\n[Worker] Shutting down gracefully.")
    except EnvironmentError as e:
        print(f"[Worker] Configuration error: {e}")
        sys.exit(1)
