from flask import Flask, request
import hmac
import hashlib
import requests
import os
import time
import base64

app = Flask(__name__)

API_KEY = "jmJVkkh4kejn86DLTKgeVQCTx1OtVji4iLf7aphJBLE="
API_SECRET = "QQKlLHrWUwfWShlOG9kYOPkC98qoDYeiKcAjl8FP2nQjzX9yxyShL4D7qZQS048xCMnnR3OEmYqgjLXir8UDVg=="
BOT_SHORT = "254dcff134ef0233f4102b75"
BOT_LONG = "254dcff134ef02332affc6c3"

def sign(payload):
    signature = hmac.new(API_SECRET.encode(), payload.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

def call_3commas(method, path):
    timestamp = str(int(time.time() * 1000))
    payload = timestamp + method + path
    url = "https://api.3commas.io" + path
    headers = {
        "X-API-Key": API_KEY,
        "X-Signature": sign(payload),
        "X-Timestamp": timestamp
    }
    if method == "POST":
        r = requests.post(url, headers=headers)
    else:
        r = requests.get(url, headers=headers)
    print(f"Status: {r.status_code}")
    print(r.text[:500])
    return r.text

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    text = data.get("text", "").upper()
    
    if "LONG" in text:
        call_3commas("POST", f"/public/api/ver1/bots/{BOT_SHORT}/disable")
        call_3commas("POST", f"/public/api/ver1/bots/{BOT_LONG}/enable")
        return "Switched to LONG", 200
    elif "SHORT" in text:
        call_3commas("POST", f"/public/api/ver1/bots/{BOT_LONG}/disable")
        call_3commas("POST", f"/public/api/ver1/bots/{BOT_SHORT}/enable")
        return "Switched to SHORT", 200
    return "Ignored", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
