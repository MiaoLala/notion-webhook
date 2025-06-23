from flask import Flask, request, jsonify
import os
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "alive"}

app = Flask(__name__)

GITHUB_REPO = "MiaoLala/notion-auto-report"
GITHUB_TOKEN = os.environ.get("GITHUB_PAT")  # Personal Access Token

@app.route("/trigger", methods=["POST"])
def trigger_action():
    event_type = request.json.get("event_type", "notion-button")
    payload = {
        "event_type": event_type,
        "client_payload": {
            "source": "notion"
        }
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(
        f"https://api.github.com/repos/{GITHUB_REPO}/dispatches",
        headers=headers,
        json=payload
    )

    if response.status_code == 204:
        return jsonify({"message": "✅ GitHub Action 已成功觸發"})
    else:
        return jsonify({
            "message": "❌ 觸發失敗",
            "status_code": response.status_code,
            "details": response.text
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
