# Aivoro — Instagram AI Bot

## Overview
An AI-powered Instagram automation bot for Aivoro. The bot automatically replies to Instagram Direct Messages and post comments using AI.

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
- Uses configurable Aivoro business context from environment variables
- Filters out echo messages and read receipts
- Skips bot's own comments (prevents infinite loop)
- Can run locally for testing or on Render for 24/7 webhook hosting

---

## Bot Knowledge

The bot uses these optional environment variables to describe the business:

| Variable | Description |
|----------|-------------|
| `BRAND_NAME` | Brand name used in replies. Defaults to `Aivoro` |
| `BUSINESS_CONTEXT` | Description of Aivoro's services and positioning |
| `WEBSITE_URL` | Website link to include when useful. Defaults to `https://aivoro.in` |

---

## Files

| File | Description |
|------|-------------|
| `main.py` | Main Flask webhook server |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |

---

## Deployment

- **GitHub Repo:** https://github.com/keerthana5463/Instagram-bot-repo
- **Live URL:** https://instagram-bot-repo.onrender.com
- **Webhook:** https://instagram-bot-repo.onrender.com/webhook

---

## Environment Variables (Render)

| Variable | Description |
|----------|-------------|
| `ACCESS_TOKEN` | Instagram API access token (refresh every 60 days) |
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `DEEPSEEK_MODEL` | Optional DeepSeek model. Defaults to `deepseek-v4-flash` |
| `INSTAGRAM_ACCOUNT_ID` | Connected Instagram account ID, used to skip bot's own comments |
| `VERIFY_TOKEN` | Webhook verification token |
| `BRAND_NAME` | Optional brand name |
| `BUSINESS_CONTEXT` | Optional business details for AI replies |
| `WEBSITE_URL` | Optional website URL |

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
$env:VERIFY_TOKEN="aivoro_instagram_webhook_2026"
$env:BRAND_NAME="Aivoro"
$env:BUSINESS_CONTEXT="Aivoro Private Limited helps businesses adopt practical AI solutions. Services include AI automation, Instagram and website chatbots, custom AI assistants, workflow automation, AI integrations for business tools, lead capture automation, customer support automation, and AI consulting for companies that want to use AI in daily operations."
$env:WEBSITE_URL="https://aivoro.in"

.\.venv\Scripts\python.exe main.py
```
