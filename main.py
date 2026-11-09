from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)
GRIZZLY_API_KEY = os.environ.get("GRIZZLY_API_KEY", "")
GRIZZLY_SMS_URL = "https://api.grizzlysms.com/agent/api/sms"
@app.route("/")
def home():
    return "GrizzlySMS Flask Provider is running", 200
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200
@app.route("/webhook", methods=["GET", "POST"])
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()
    phone = data.get("phone") or data.get("number") or data.get("to") or data.get("from") or ""
    text = data.get("message") or data.get("text") or data.get("body") or ""
    if phone and text and GRIZZLY_API_KEY:
        try:
            payload = {"key": GRIZZLY_API_KEY, "phone": phone, "number": phone, "message": text, "text": text}
            requests.post(GRIZZLY_SMS_URL, json=payload, timeout=10)
        except Exception as e:
            print(e, flush=True)
    return jsonify({"status": "ok"}), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
