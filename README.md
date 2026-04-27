# BTNL Instagram AI Bot

## Overview
An AI-powered Instagram automation bot for BTNL - Bangalore Technology Network Pvt. Ltd. The bot automatically replies to Instagram Direct Messages and post comments using AI.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + Flask | Webhook server |
| Meta Graph API | Receive Instagram DMs and Comments |
| DeepSeek API | AI reply generation |
| Render.com | Free cloud hosting |
| GitHub | Code repository |

---

## How It Works

### DM Auto-Reply:
1. User sends a DM to your connected Instagram account
2. Meta sends the message to our webhook (Render server)
3. Flask receives the message
4. DeepSeek generates a smart, personalized reply
5. Reply is sent back to the user via Instagram API — all in seconds!

### Comment Auto-Reply:
1. User comments on your connected Instagram account's post
2. Meta sends the comment to our webhook
3. Flask detects it's a comment (not a DM)
4. DeepSeek generates a short, public-friendly reply
5. Reply is posted under the comment automatically!

---

## Features

- Auto-replies to all Instagram DMs 24/7
- Auto-replies to all Instagram Post Comments 24/7
- AI-generated responses (not fixed templates)
- Replies in the same language as the user
- Uses configurable BTNL business context from environment variables
- Detects Instagram DM lead/support details and exposes a simple daily lead report
- Filters out echo messages and read receipts
- Skips bot's own comments (prevents infinite loop)
- Can run locally for testing or on Render for 24/7 webhook hosting

---

## Bot Knowledge

The bot uses these optional environment variables to describe the business:

| Variable | Description |
|----------|-------------|
| `BRAND_NAME` | Brand name used in replies |
| `BUSINESS_CONTEXT` | Description of BTNL services, support flow, lead qualification fields, contact details, pricing guidance, and call to action |
| `WEBSITE_URL` | Website link to include when useful |

---

## Files

| File | Description |
|------|-------------|
| `main.py` | Main Flask webhook server |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |
| `.env.example` | Environment variable template for each new customer |
| `FACEBOOK_META_SETUP.md` | Meta/Facebook setup checklist |
| `LEAD_REPORT_SETUP.md` | Simple daily lead report setup |

---

## Deployment

- **GitHub Repo:** https://github.com/anildandina08012025/InstagramBotAI
- **Webhook Path:** `/webhook`

---

## Environment Variables (Render)

| Variable | Description |
|----------|-------------|
| `ACCESS_TOKEN` | Instagram API access token (refresh every 60 days) |
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `DEEPSEEK_MODEL` | Optional DeepSeek model. Defaults to `deepseek-v4-flash` |
| `INSTAGRAM_ACCOUNT_ID` | Connected Instagram account ID, used to skip the bot's own comments |
| `VERIFY_TOKEN` | Webhook verification token |
| `BRAND_NAME` | Recommended: `BTNL` |
| `BUSINESS_CONTEXT` | BTNL service and lead-capture details for AI replies |
| `WEBSITE_URL` | Recommended: `https://btnl.in` |
| `LEAD_LOG_ENABLED` | Set to `true` to detect and log leads |
| `LEADS_REPORT_TOKEN` | Private token for `/leads/today` report |
| `LOCAL_TIMEZONE` | Defaults to `Asia/Kolkata` |

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `No module named 'app'` | Wrong start command | Set start command to `gunicorn main:app` in Render |
| `No module named 'google'` | Wrong package installed | Use `google-generativeai` OR `google-genai` — must match import in main.py |
| `Invalid OAuth access token` | Token expired or wrong endpoint | Regenerate token from Meta Developer Console → update Render env variable |
| `Cannot parse access token` | Using Facebook token with Instagram API | Use `graph.instagram.com` not `graph.facebook.com` for IGAA tokens |
| `DeepSeek 401/403` | Wrong or missing DeepSeek API key | Set `DEEPSEEK_API_KEY` correctly |
| `Model not found (404)` | Wrong model name or API endpoint | Check the model in `generate_deepseek_reply()` |
| `Webhook not receiving events` | App in development/unpublished mode | Publish the app in Meta Developer Console |
| `Bot replying to own DMs` | Echo messages not filtered | Add `is_echo` check in receive_message() |
| `Bot spamming 50+ comments` | Bot replying to own comments | Set `INSTAGRAM_ACCOUNT_ID` to your connected Instagram account ID |
| `Render sleeps after 15 min` | Free tier spin-down | Set up UptimeRobot to ping every 5 minutes |

---

## Important Notes

- Instagram Access Token expires every **60 days** — must be refreshed manually
- Render free tier sleeps after 15 min inactivity — set up UptimeRobot to keep it alive
- Instagram account ID is used to filter bot's own comments
- `comments` webhook field must be **Subscribed** in Meta Developer Console
- Webhook Subscription must be **ON** for your connected Instagram account

---

## Local Run

```powershell
$env:ACCESS_TOKEN="your_instagram_access_token"
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
$env:DEEPSEEK_MODEL="deepseek-v4-flash"
$env:INSTAGRAM_ACCOUNT_ID="17841427765061331"
$env:VERIFY_TOKEN="unique_customer_verify_token"
$env:BRAND_NAME="BTNL"
$env:BUSINESS_CONTEXT="BTNL stands for Bangalore Technology Network Pvt. Ltd. BTNL provides enterprise internet, leased line, business broadband, managed WiFi, networking, firewall, CCTV, cloud, IPPBX, SIP, cybersecurity and IT infrastructure solutions. Collect lead details and guide users toward a quote or callback. For urgent support, ask them to call +91 9686656005 or 7204656005. Do not promise exact price, installation time or guaranteed SLA unless confirmed by BTNL."
$env:WEBSITE_URL="https://btnl.in"
$env:LEAD_LOG_ENABLED="true"
$env:LEADS_REPORT_TOKEN="private_report_token"
$env:LOCAL_TIMEZONE="Asia/Kolkata"

.\.venv\Scripts\python.exe main.py
```

For the Meta/Facebook configuration steps, follow `FACEBOOK_META_SETUP.md`.
For the simple daily lead report, follow `LEAD_REPORT_SETUP.md`.
