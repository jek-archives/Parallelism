import os
import time
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, request
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from shared.queue_manager import get_queue

load_dotenv()

app = Flask(__name__)
vote_queue = get_queue()

REQUIRED_FIELDS = {"user_id", "poll_id", "choice", "edge_id", "timestamp"}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "queue_size": vote_queue.qsize()}), 200


@app.route("/vote", methods=["POST"])
def submit_vote():
    data = request.get_json(silent=True)


    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return jsonify({"error": f"Missing required fields: {sorted(missing)}"}), 400

    if not isinstance(data["timestamp"], (int, float)):
        return jsonify({"error": "'timestamp' must be a number"}), 400


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
    return jsonify({"queue_size": vote_queue.qsize()}), 200


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    print(f"[API] Starting Flask on port {port}  debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)
