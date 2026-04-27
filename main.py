from flask import Flask, request, jsonify
import requests
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "change_me_unique_verify_token")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
INSTAGRAM_ACCOUNT_ID = os.environ.get("INSTAGRAM_ACCOUNT_ID", "")
BRAND_NAME = os.environ.get("BRAND_NAME", "BTNL")
BUSINESS_CONTEXT = os.environ.get(
    "BUSINESS_CONTEXT",
    (
        "BTNL stands for Bangalore Technology Network Pvt. Ltd. "
        "BTNL provides enterprise internet, dedicated leased line internet, business broadband, "
        "1:1 bandwidth connectivity, secure private connectivity, dual last-mile backup, "
        "fiber point-to-point connectivity, managed office WiFi, campus WiFi, guest WiFi, "
        "networking, routers, switches, firewalls, CCTV, IT security infrastructure, cloud, "
        "servers, IPPBX, SIP telephone lines, intercom, VoIP over WiFi, CRM, POS, ERP, LMS, "
        "cybersecurity and cloud services for businesses. "
        "BTNL serves corporate offices, IT companies, startups, SMEs, warehouses, factories, "
        "colleges, hostels, healthcare, retail, e-commerce, co-working spaces, multi-branch "
        "businesses and enterprises. "
        "Key value propositions: reliable high-speed business internet, 24/7 support, "
        "enterprise-grade security, low latency, SLA-backed uptime where applicable, "
        "redundant network design, proactive monitoring, NOC-based issue detection, "
        "network failover and custom solutions. "
        "For leads, collect name, company, phone, email, location, business type, service "
        "required, number of users/devices, current issue, required bandwidth and preferred "
        "callback time. "
        "For support issues such as slow internet or downtime, collect company name, "
        "registered phone, location, issue type, when it started, whether internet is fully "
        "down or slow, and router/access point light status. For urgent help ask them to call "
        "+91 9686656005 or 7204656005. "
        "Do not promise exact price, installation time or guaranteed SLA unless confirmed by "
        "BTNL. For pricing, say it depends on location, bandwidth, service type and business "
        "requirement, and BTNL can provide a custom quote. "
        "Contact: No.68, 3rd Floor, MM Road, Frazer Town, Bengaluru, Karnataka 560005. "
        "Phone: +91 9686656005 / 7204656005. Email: vimalraj@btnl.co.in."
    )
)
WEBSITE_URL = os.environ.get("WEBSITE_URL", "https://btnl.in")
LEAD_LOG_ENABLED = os.environ.get("LEAD_LOG_ENABLED", "true").lower() == "true"
LEAD_LOG_FILE = os.environ.get("LEAD_LOG_FILE", "leads_log.jsonl")
LEADS_REPORT_TOKEN = os.environ.get("LEADS_REPORT_TOKEN", "")
LOCAL_TIMEZONE = ZoneInfo(os.environ.get("LOCAL_TIMEZONE", "Asia/Kolkata"))

DM_SYSTEM_PROMPT = f"""You are the Instagram DM assistant for {BRAND_NAME}.
About {BRAND_NAME}:
{BUSINESS_CONTEXT}
Website: {WEBSITE_URL or "Not provided"}

DM goal:
Your first priority is to convert the DM conversation into a qualified BTNL lead or support handoff.

How to reply:
- Sound like a professional BTNL assistant, not a generic AI bot.
- Keep replies under 80 words.
- Answer in the same language as the customer.
- Start by understanding the requirement: leased line, office internet, WiFi, firewall/networking, IPPBX/SIP, guest WiFi, quote, or support issue.
- If the customer asks a service question, answer briefly and then move toward lead capture.
- Ask only 1-2 questions per message so the conversation feels natural.
- Do not ask for all details at once.

Lead capture order:
1. Name and phone number
2. Company name and location
3. Service required and number of users/devices
4. Current issue or required bandwidth
5. Email and preferred callback time

Support flow:
- If internet is slow/down or they need support, collect company name, registered phone, location, issue type, when it started, down/slow status, and router/access point light status.
- For urgent support, share: +91 9686656005 / 7204656005.

Rules:
- Do not promise exact price, installation time, or guaranteed SLA.
- For pricing, say pricing depends on location, bandwidth, service type and requirement; BTNL can provide a custom quote.
- End most replies with a clear next step such as sharing phone number, company/location, or asking if BTNL should call."""

COMMENT_SYSTEM_PROMPT = f"""You are the public Instagram comment assistant for {BRAND_NAME}.
About {BRAND_NAME}:
{BUSINESS_CONTEXT}
Website: {WEBSITE_URL or "Not provided"}

Comment goal:
Reply helpfully in public, but move detailed lead capture to DM or phone.

Reply rules:
- Keep replies under 45 words.
- Be friendly, positive and professional.
- Answer in the same language as the comment.
- If they ask about leased line, WiFi, networking, firewall, cloud or support, give a short relevant answer.
- Do NOT ask for phone, email, address, account details, or sensitive details publicly.
- Invite them to DM BTNL for a quote/callback, or call +91 9686656005 / 7204656005 for urgent support.
- Do NOT use bullet points."""

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "instagram-bot",
        "brand": BRAND_NAME
    }), 200

@app.route("/leads/today", methods=["GET"])
def leads_today():
    if not LEADS_REPORT_TOKEN:
        return jsonify({"error": "LEADS_REPORT_TOKEN is not configured"}), 403

    token = request.args.get("token", "")
    if token != LEADS_REPORT_TOKEN:
        return jsonify({"error": "Forbidden"}), 403

    today = datetime.now(LOCAL_TIMEZONE).date().isoformat()
    leads = read_leads_for_date(today)
    return jsonify({
        "date": today,
        "timezone": str(LOCAL_TIMEZONE),
        "count": len(leads),
        "leads": leads
    }), 200

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
    data = request.get_json(silent=True) or {}
    print(f"Received: {data}")
    try:
        for entry in data.get("entry", []):
            # Handle DMs. Instagram can also send read receipts, edits, and other
            # messaging events here; only new text messages should get replies.
            for messaging in entry.get("messaging", []):
                if any(key in messaging for key in ("read", "message_edit", "delivery", "postback")):
                    print(f"Skipping non-reply messaging event with keys: {list(messaging.keys())}")
                    continue

                message_obj = messaging.get("message", {})
                if not message_obj:
                    print(f"Skipping unsupported messaging event with keys: {list(messaging.keys())}")
                    continue

                if message_obj.get("is_echo"):
                    print("Skipping echo message")
                    continue

                sender_id = messaging.get("sender", {}).get("id")
                message = message_obj.get("text", "")
                if not sender_id or not message:
                    print("Skipping messaging event without sender/text")
                    continue

                capture_lead_if_available(sender_id, message)
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

def generate_deepseek_reply(user_message, system_prompt, max_tokens=150):
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
        "max_tokens": max_tokens,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    print(f"DeepSeek response: {result}")
    return result["choices"][0]["message"]["content"]

def capture_lead_if_available(sender_id, message):
    if not LEAD_LOG_ENABLED:
        return

    try:
        lead = extract_lead_details(sender_id, message)
        if not lead.get("should_save"):
            print("No lead details found in message")
            return

        save_lead(lead)
    except Exception as e:
        # Do not block Instagram replies if lead capture fails.
        print(f"Lead capture failed: {e}")

def extract_lead_details(sender_id, message):
    extraction_prompt = """Extract BTNL Instagram lead/support details from the user's latest message.
Return only valid JSON. Do not include markdown.
Use empty strings when unknown.
Set should_save to true only if the message contains at least one useful contact or business detail such as name, company, phone, email, location, service, issue, bandwidth, users/devices, callback time, or a support problem.
Set lead_type to one of: sales_lead, support_request, general_inquiry.
Fields:
should_save, lead_type, name, company, phone, email, location, business_type, service_required, users_or_devices, current_issue, required_bandwidth, preferred_callback_time, notes"""

    raw = generate_deepseek_reply(message, extraction_prompt, max_tokens=400)
    lead = json.loads(extract_json_object(raw))
    lead["instagram_sender_id"] = sender_id
    lead["source"] = "instagram_dm"
    lead["message"] = message
    lead["created_at"] = datetime.now(LOCAL_TIMEZONE).isoformat()
    lead["created_date"] = datetime.now(LOCAL_TIMEZONE).date().isoformat()
    return lead

def extract_json_object(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON object found in extraction response: {text}")

    return cleaned[start:end + 1]

def save_lead(lead):
    line = json.dumps(lead, ensure_ascii=True)
    with open(LEAD_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(line + "\n")
    print(f"LEAD_CAPTURED: {line}")

def read_leads_for_date(date_text):
    if not os.path.exists(LEAD_LOG_FILE):
        return []

    leads = []
    with open(LEAD_LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            try:
                lead = json.loads(line)
            except json.JSONDecodeError:
                continue

            if lead.get("created_date") == date_text:
                leads.append(lead)

    return leads

def send_instagram_reply(recipient_id, message):
    if not ACCESS_TOKEN:
        raise ValueError("ACCESS_TOKEN environment variable is not set")

    url = "https://graph.instagram.com/v21.0/me/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"DM Reply sent: {response.status_code} - {response.text}")
    response.raise_for_status()

def reply_to_comment(comment_id, message):
    if not ACCESS_TOKEN:
        raise ValueError("ACCESS_TOKEN environment variable is not set")

    url = f"https://graph.instagram.com/v21.0/{comment_id}/replies"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {"message": message}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Comment Reply sent: {response.status_code} - {response.text}")
    response.raise_for_status()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
