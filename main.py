from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "") or ""
    phone = ""
    if text.startswith("From:"):
        parts = text.split(chr(10), 1)
        if len(parts) == 2:
            phone = parts[0].replace("From", "").replace(":", "").strip()
            text = parts[1].strip()
    print(f"RECEIVED phone={phone} text={text}", flush=True)
    return jsonify({"status": "ok"}), 200
@app.route("/", methods=["GET"])
def home():
    return "OK", 200