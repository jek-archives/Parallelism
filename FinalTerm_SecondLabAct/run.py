import threading
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()


def start_api():
    from api.app import app
    port  = int(os.getenv("API_PORT", 5000))
    debug = False
    print(f"[Launcher] Flask API starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)


def start_worker():
    from worker.worker import run_worker
    print("[Launcher] Worker starting…")
    run_worker()


if __name__ == "__main__":
    api_thread    = threading.Thread(target=start_api,    daemon=True, name="api")
    worker_thread = threading.Thread(target=start_worker, daemon=False, name="worker")

    api_thread.start()
    worker_thread.start()

    print("[Launcher] Both components running. Press Ctrl+C to stop.")
    try:
        worker_thread.join()
    except KeyboardInterrupt:
        print("\n[Launcher] Shutting down.")
