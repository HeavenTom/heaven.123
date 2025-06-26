from flask import Flask, request
import requests
import os

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "verai123token")

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Incoming message from Meta:", data)

    # Make.com Webhook URL
    make_url = "https://hook.eu2.make.com/h37ptg8j5uwyyvm6bv714vy5837f2tqr"
    headers = {"Content-Type": "application/json"}

    try:
        # Send data to Make.com
        response = requests.post(make_url, json=data, headers=headers)
        
        # Log the response status and content from Make
        print(f"✅ Sent to Make.com: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Failed to send to Make.com: {e}")

    return "ok", 200

if __name__ == "__main__":
    app.run()
