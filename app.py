import os
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

FILTERS_FILE = "filters.json"

@app.route("/")
def index():
    try:
        with open(FILTERS_FILE, "r") as f:
            filters = json.load(f)
    except:
        filters = []
    return jsonify({"filters": filters})

@app.route("/scrape", methods=["GET"])
def scrape():
    # Simule un scraping ici (vraie logique à intégrer)
    return jsonify({"status": "ok", "message": "Scraping lancé (simulation)."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
