"""
Football Ultimate - shared online server
==========================================
This is a tiny web server that stores everyone's accounts (including
friends and trade requests) and the transfer market in ONE shared place
online, instead of on each person's own computer.
"""

import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

SAVES_FILE = "saves.json"
MARKET_FILE = "market.json"


def read_json_file(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def write_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/saves", methods=["GET"])
def get_saves():
    return jsonify(read_json_file(SAVES_FILE, {}))


@app.route("/saves", methods=["POST"])
def post_saves():
    data = request.get_json(force=True)
    write_json_file(SAVES_FILE, data)
    return jsonify({"status": "ok"})


@app.route("/market", methods=["GET"])
def get_market():
    return jsonify(read_json_file(MARKET_FILE, []))


@app.route("/market", methods=["POST"])
def post_market():
    data = request.get_json(force=True)
    write_json_file(MARKET_FILE, data)
    return jsonify({"status": "ok"})


@app.route("/")
def index():
    return "Football Ultimate server is running."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
