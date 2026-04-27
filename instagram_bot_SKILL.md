# Skill Report — Aivoro Instagram AI Bot

## Project

Aivoro Instagram DM + Comment Automation

## Skills Demonstrated

### API Integration

- Connected Meta Instagram webhooks for DMs and comment events.
- Integrated DeepSeek through the OpenAI-compatible chat completions API.
- Used Instagram Graph API endpoints to send DM replies and comment replies.
- Kept API keys and access tokens in Render environment variables instead of source code.

### Backend Development

- Built a Flask webhook server.
- Implemented Meta webhook verification through `hub.challenge`.
- Handled multiple webhook entries and multiple messaging events.
- Skipped non-reply events such as read receipts, message edits, deliveries, postbacks, and echoes.
- Added separate prompts for DMs and public comments.
- Added a health route for Render and business-login redirects.

### Cloud Deployment

- Deployed the bot on Render as a Python web service.
- Connected GitHub for deployment from the `main` branch.
- Configured `gunicorn main:app` as the start command.
- Used Render logs to debug webhook payloads and API errors.

### Meta Developer Platform

- Created a Meta app for `AivoroIBot`.
- Added required Instagram permissions:
  - `instagram_business_basic`
  - `instagram_business_manage_messages`
  - `instagram_manage_comments`
- Connected the Instagram account `@anil_ai_trend`.
- Configured the webhook callback URL:
  - `https://instagrambotai.onrender.com/webhook`
- Turned on webhook subscription for the connected Instagram account.

## Current Architecture

```text
Instagram DM/comment
        |
        v
Meta Instagram Webhook
        |
        v
Render Flask App (/webhook)
        |
        +--> Skip read/edit/delivery/echo events
        |
        +--> DeepSeek generates Aivoro reply
        |
        +--> Instagram Graph API sends DM/comment reply
```

## Lessons From Debugging

- `message_edit` webhook events do not include `sender`, so they must be skipped.
- Meta webhook verification only proves the callback URL works; real DMs require a `POST /webhook`.
- If the app is unpublished, only admins/testers should be used for testing.
- Free Render instances can sleep, delaying webhook responses after inactivity.
- Tokens exposed in local files or chat should be rotated.

