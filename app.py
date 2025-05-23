import os
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Tarte aux pommes est en ligne."})

@app.route("/scrape", methods=["GET"])
def scrape():
    try:
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        return jsonify({
            "status": "done",
            "stdout": result.stdout,
            "stderr": result.stderr
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
