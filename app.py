from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GITHUB_REPO = "MiaoLala/notion-auto-report"
GITHUB_TOKEN = os.environ.get("GITHUB_PAT")  # Personal Access Token

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "alive"})
    
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
    port = int(os.environ.get("PORT", 5000))  # Render 會提供 PORT 環境變數
    app.run(host="0.0.0.0", port=port)
