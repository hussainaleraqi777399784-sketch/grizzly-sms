
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "SMS Server is Running", 200


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    data = request.get_json(silent=True) or {}
    payload = data.get("payload") or {}

    phone = (
        payload.get("phoneNumber")
        or payload.get("sender")
        or request.values.get("from")
        or request.values.get("phone")
        or ""
    )

    message = (
        payload.get("message")
        or request.values.get("msg")
        or request.values.get("text")
        or request.values.get("message")
        or ""
    )

    print("========== NEW SMS ==========", flush=True)
    print(f"PHONE: {phone}", flush=True)
    print(f"MESSAGE: {message}", flush=True)
    print("=============================", flush=True)

    return jsonify({
        "status": "success",
        "phone": phone,
        "text": message
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
