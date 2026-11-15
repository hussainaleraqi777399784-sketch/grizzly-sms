from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("=== NEW REQUEST ===", flush=True)
    print(f"METHOD={request.method}", flush=True)
    try:
        raw = request.get_data(as_text=True) or ""
    except:
        raw = ""
    print(f"RAW={raw}", flush=True)
    data = request.get_json(force=True, silent=True) or {}
    print(f"JSON={data}", flush=True)
    phone = data.get("phone") or data.get("phoneNumber") or data.get("number") or data.get("from") or data.get("sender") or ""
    text = data.get("text") or data.get("msg") or data.get("message") or data.get("body") or ""
    if not text and raw:
        text = raw
    if text and "From" in text:
        parts = text.split(chr(10), 1)
        if len(parts) == 2:
            phone = parts[0].replace("From", "").replace(":", "").strip()
            text = parts[1].strip()
    if phone in ("{from}", "text-", "", None):
        phone = ""
    print(f"RECEIVED phone={phone} text={text}", flush=True)
    print(f"FINAL_TEXT_TO_GRIZZLY={text}", flush=True)
    return jsonify({"status": "ok", "phone": phone, "text": text}), 200
@app.route("/", methods=["GET"])
def home():
    return "OK", 200