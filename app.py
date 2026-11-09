from flask import Flask, request
import hmac
import hashlib
import requests
import os

app = Flask(__name__)

API_KEY = "jmJVkkh4kejn86DLTKgeVQCTx1OtVji4iLf7aphJBLE="
API_SECRET = "QQKlLHrWUwfWShlOG9kYOPkC98qoDYeiKcAjl8FP2nQjzX9yxyShL4D7qZQS048xCMnnR3OEmYqgjLXir8UDVg=="
BOT_SHORT = "254dcff134ef0233f4102b75"
BOT_LONG = "254dcff134ef02332affc6c3"

def sign(path, data=""):
    msg = path
    if data:
        msg += data
    return hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()

def call_3commas(method, path):
    url = "https://api.3commas.io" + path
    headers = {
        "APIKEY": API_KEY,
        "Signature": sign(path)
    }
    if method == "POST":
        r = requests.post(url, headers=headers)
    else:
        r = requests.get(url, headers=headers)
    print(r.text)  
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
