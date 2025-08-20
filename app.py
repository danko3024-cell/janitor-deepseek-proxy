from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com/v1/chat/completions"

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = request.get_json()
    response = requests.post(BASE_URL, headers=headers, json=data)
    return (response.text, response.status_code, response.headers.items())

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "DeepSeek Proxy running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
