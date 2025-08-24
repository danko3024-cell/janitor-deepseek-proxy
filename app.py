from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os

app = Flask(__name__)
CORS(app)  # <--- очень важно

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route("/")
def home():
    return jsonify({"status": "DeepSeek proxy is running"})

@app.route("/v1/chat/completions", methods=["POST"])
def proxy():
    data = request.json
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    return (resp.text, resp.status_code, resp.headers.items())
