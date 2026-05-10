"""
app.py
------
Flask API server.  Accepts POST /vote requests from edge nodes,
validates the payload, and enqueues it for asynchronous processing.

Start with:
    python api/app.py
"""

import os
import time
import sys

# Allow sibling-package imports when running from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from shared.queue_manager import get_queue

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

load_dotenv()

app = Flask(__name__)
vote_queue = get_queue()          # Shared in-process queue

REQUIRED_FIELDS = {"user_id", "poll_id", "choice", "edge_id", "timestamp"}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Simple liveness probe."""
    return jsonify({"status": "ok", "queue_size": vote_queue.qsize()}), 200


@app.route("/vote", methods=["POST"])
def submit_vote():
    """
    Accept a vote from an edge node.

    Expected JSON body:
        {
            "user_id":   "user_001",
            "poll_id":   "poll_mayor",
            "choice":    "Alice",
            "edge_id":   "edge-1",
            "timestamp": 1715000000.123    # Unix epoch from the edge node
        }

    Returns:
        200 – vote enqueued
        400 – missing / invalid fields
        500 – unexpected server error
    """
    data = request.get_json(silent=True)

    # ── Validation ──────────────────────────────────────────────────────────
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return jsonify({"error": f"Missing required fields: {sorted(missing)}"}), 400

    if not isinstance(data["timestamp"], (int, float)):
        return jsonify({"error": "'timestamp' must be a number"}), 400

    # ── Enqueue ─────────────────────────────────────────────────────────────
    vote = {
        "user_id":   str(data["user_id"]),
        "poll_id":   str(data["poll_id"]),
        "choice":    str(data["choice"]),
        "edge_id":   str(data["edge_id"]),
        "timestamp": float(data["timestamp"]),
    }

    vote_queue.put(vote)

    queue_size = vote_queue.qsize()
    app.logger.info(
        "Enqueued vote user=%s poll=%s edge=%s  queue_size=%d",
        vote["user_id"], vote["poll_id"], vote["edge_id"], queue_size,
    )

    return jsonify({
        "status":     "queued",
        "queue_size": queue_size,
        "vote_id":    f"{vote['user_id']}_{vote['poll_id']}",
    }), 200


@app.route("/queue/size", methods=["GET"])
def queue_size():
    """Expose current queue depth (useful for monitoring during fault tests)."""
    return jsonify({"queue_size": vote_queue.qsize()}), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    print(f"[API] Starting Flask on port {port}  debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)
