from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "aivoro_instagram_webhook_2026")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "17841427765061331")
BRAND_NAME = os.environ.get("BRAND_NAME", "Aivoro")
BUSINESS_CONTEXT = os.environ.get(
    "BUSINESS_CONTEXT",
    (
        "Aivoro Private Limited helps businesses adopt practical AI solutions. "
        "Services include AI automation, Instagram and website chatbots, custom AI assistants, "
        "workflow automation, AI integrations for business tools, lead capture automation, "
        "customer support automation, and AI consulting for companies that want to use AI in daily operations. "
        "Aivoro focuses on building useful, business-ready AI systems instead of generic demos."
    )
)
WEBSITE_URL = os.environ.get("WEBSITE_URL", "https://aivoro.in")

DM_SYSTEM_PROMPT = f"""You are a helpful Instagram assistant for {BRAND_NAME}.
About {BRAND_NAME}:
{BUSINESS_CONTEXT}
Website: {WEBSITE_URL or "Not provided"}
Reply rules:
- Keep replies short under 80 words
- Be friendly and helpful
- Answer in the same language they message in
- Always end with a soft call to action"""

COMMENT_SYSTEM_PROMPT = f"""You are a helpful Instagram assistant for {BRAND_NAME}.
About {BRAND_NAME}:
{BUSINESS_CONTEXT}
Website: {WEBSITE_URL or "Not provided"}
Reply rules:
- Keep replies very short under 50 words (it's a public comment!)
- Be friendly, positive and professional
- Answer in the same language as the comment
- Always end with a soft call to action
- Do NOT use bullet points in comments"""

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified!")
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json
    print(f"Received: {data}")
    try:
        for entry in data.get("entry", []):
            # Handle DMs. Instagram can also send read receipts, edits, and other
            # messaging events here; only new text messages should get replies.
            for messaging in entry.get("messaging", []):
                if "read" in messaging or "message_edit" in messaging:
                    print("Skipping non-reply messaging event")
                    continue

                message_obj = messaging.get("message", {})
                if message_obj.get("is_echo"):
                    print("Skipping echo message")
                    continue

                sender_id = messaging.get("sender", {}).get("id")
                message = message_obj.get("text", "")
                if not sender_id or not message:
                    print("Skipping messaging event without sender/text")
                    continue

                reply = generate_deepseek_reply(message, DM_SYSTEM_PROMPT)
                send_instagram_reply(sender_id, reply)

            # Handle Comments
            for change in entry.get("changes", []):
                if change.get("field") == "comments":
                    value = change.get("value", {})
                    comment_text = value.get("text", "")
                    comment_id = value.get("id", "")
                    commenter_id = value.get("from", {}).get("id", "")
                    username = value.get("from", {}).get("username", "")

                    # Skip bot's own comments
                    if commenter_id == INSTAGRAM_ACCOUNT_ID:
                        print(f"Skipping own comment from @{username}")
                        continue

                    print(f"New comment from @{username}: {comment_text}")
                    if comment_text and comment_id:
                        reply = generate_deepseek_reply(comment_text, COMMENT_SYSTEM_PROMPT)
                        reply_to_comment(comment_id, reply)

    except Exception as e:
        print(f"Error: {e}")
    return jsonify({"status": "ok"}), 200

def generate_deepseek_reply(user_message, system_prompt):
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY environment variable is not set")

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 150,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    print(f"DeepSeek response: {result}")
    return result["choices"][0]["message"]["content"]

def send_instagram_reply(recipient_id, message):
    url = "https://graph.instagram.com/v21.0/me/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"DM Reply sent: {response.status_code} - {response.text}")

def reply_to_comment(comment_id, message):
    url = f"https://graph.instagram.com/v21.0/{comment_id}/replies"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {"message": message}
    response = requests.post(url, headers=headers, json=payload)
    print(f"Comment Reply sent: {response.status_code} - {response.text}")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
