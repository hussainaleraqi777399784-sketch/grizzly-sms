
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "SMS Server is Running", 200


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    data = request.get_json(silent=True) or {}

    phone = (
        request.values.get("from")
        or data.get("from")
        or data.get("phone")
        or ""
    )

    message = (
        request.values.get("msg")
        or request.values.get("text")
        or data.get("msg")
        or data.get("text")
        or data.get("message")
        or ""
    )

    print(f"RECEIVED phone={phone}", flush=True)
    print(f"RECEIVED text={message}", flush=True)

    return jsonify({
        "status": "success",
        "phone": phone,
        "text": message
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
