from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    phone = data.get("phone") or data.get("phoneNumber") or data.get("number") or data.get("from") or ""
    text = data.get("text") or data.get("msg") or data.get("message") or ""
    if phone in ("{from}", "text-", "", None):
        phone = ""
    if text and "From" in text:
        t = text.replace("From:", "").replace("From", "").strip()
        parts = t.split()
        if len(parts) >= 1 and not phone:
            phone = parts[0].strip()
        if len(parts) >= 2:
            text = " ".join(parts[1:]).strip()
        elif len(parts) == 1:
            text = ""
    print(f"RECEIVED phone={phone} text={text}", flush=True)
    return jsonify({"status": "ok", "phone": phone, "text": text}), 200
@app.route("/", methods=["GET"])
def home():
    return "OK", 200