from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # позволяем запросы из браузера (Janitor)

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Together Proxy running!"})


@app.route("/v1/chat/completions", methods=["POST"])
def proxy():
    if not TOGETHER_API_KEY:
        return jsonify({"error": "TOGETHER_API_KEY is not set on the server"}), 500

    data = request.get_json(force=True) or {}

    # На всякий случай выключим стрим, чтобы ответ был обычным JSON
    if data.get("stream") is True:
        data["stream"] = False

    # Если модель не указали — подставим дефолтную
    data.setdefault("model", "mistralai/Mixtral-8x7B-Instruct-v0.1")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(TOGETHER_URL, headers=headers, json=data, timeout=60)
        # Пробрасываем ответ как есть
        return (resp.text, resp.status_code, resp.headers.items())
    except Exception as e:
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    # локально 5000, на Render порт придёт в переменной PORT
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
