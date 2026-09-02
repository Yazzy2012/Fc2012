"""
Football Ultimate - shared online server
==========================================
This is a tiny web server that stores everyone's accounts (including
friends and trade requests) and the transfer market in ONE shared place
online, instead of on each person's own computer.

Data is stored in a Firebase Realtime Database instead of a local JSON
file on this server's disk. This matters because Render's free tier does
NOT persist local disk writes across restarts/redeploys - the old
version (writing to saves.json on disk) would silently lose every
account whenever the free instance spun down and back up. Firebase is a
separate, always-on service, so the data survives regardless of what
happens to this server process.
"""

import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your Firebase Realtime Database URL (no trailing slash).
FIREBASE_URL = "https://fc2012-default-rtdb.firebaseio.com"

# Firebase REST API convention: append ".json" to the path you want to
# read/write. "/saves.json" reads/writes everything under the "saves" node.
SAVES_URL = f"{FIREBASE_URL}/saves.json"
MARKET_URL = f"{FIREBASE_URL}/market.json"


def read_from_firebase(url, default):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data if data is not None else default
    except Exception as e:
        print(f"Firebase read failed for {url}: {e}")
        return default


def write_to_firebase(url, data):
    try:
        resp = requests.put(url, json=data, timeout=15)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"Firebase write failed for {url}: {e}")
        return False


@app.route("/saves", methods=["GET"])
def get_saves():
    return jsonify(read_from_firebase(SAVES_URL, {}))


@app.route("/saves", methods=["POST"])
def post_saves():
    data = request.get_json(force=True)
    ok = write_to_firebase(SAVES_URL, data)
    if not ok:
        return jsonify({"status": "error", "message": "Could not reach Firebase"}), 502
    return jsonify({"status": "ok"})


@app.route("/market", methods=["GET"])
def get_market():
    return jsonify(read_from_firebase(MARKET_URL, []))


@app.route("/market", methods=["POST"])
def post_market():
    data = request.get_json(force=True)
    ok = write_to_firebase(MARKET_URL, data)
    if not ok:
        return jsonify({"status": "error", "message": "Could not reach Firebase"}), 502
    return jsonify({"status": "ok"})


@app.route("/")
def index():
    return "Football Ultimate server is running."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
