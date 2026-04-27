# Aivoro Instagram AI Bot Notes

## Current Stack

| Tool | Purpose |
|------|---------|
| Python + Flask | Webhook server |
| Meta Instagram API | Receive Instagram DMs and comments |
| DeepSeek API | Generate AI replies |
| Render | Host the public webhook |
| GitHub | Source repository and Render deploy trigger |

## Live Configuration

- GitHub repo: `https://github.com/anildandina08012025/InstagramBotAI`
- Render service URL: `https://instagrambotai.onrender.com`
- Webhook URL: `https://instagrambotai.onrender.com/webhook`
- Verify token: `aivoro_instagram_webhook_2026`
- Instagram account ID: `17841427765061331`

## Required Render Environment Variables

| Variable | Purpose |
|----------|---------|
| `ACCESS_TOKEN` | Instagram API access token |
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `DEEPSEEK_MODEL` | Recommended: `deepseek-v4-flash` |
| `INSTAGRAM_ACCOUNT_ID` | Bot account ID used to skip own comments |
| `VERIFY_TOKEN` | Meta webhook verification token |
| `BRAND_NAME` | Recommended: `Aivoro` |
| `BUSINESS_CONTEXT` | Aivoro service knowledge used by the AI |
| `WEBSITE_URL` | Recommended: `https://aivoro.in` |

## Important Runtime Behavior

- The bot replies only to new text DMs.
- It skips read receipts, message edits, delivery events, postbacks, and echo messages.
- It replies to Instagram post comments when Meta sends `comments` webhook events.
- It skips comments from its own Instagram account to avoid loops.
- `/` is a health endpoint.
- `/webhook` is the Meta webhook endpoint.

## Common Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `Error: 'sender'` | A non-message event such as `message_edit` was treated as a DM | Fixed by skipping non-reply messaging events |
| `ACCESS_TOKEN environment variable is not set` | Render is missing the Instagram token | Add/update `ACCESS_TOKEN` in Render |
| `DEEPSEEK_API_KEY environment variable is not set` | Render is missing DeepSeek key | Add/update `DEEPSEEK_API_KEY` in Render |
| `401/403` from DeepSeek | Wrong/expired DeepSeek key or no credits/access | Rotate key and update Render |
| `400/401` from Instagram send endpoint | Expired token or missing permission | Regenerate Instagram token and update Render |
| No `POST /webhook` in Render logs | Meta is not sending events | Check webhook subscription, tester roles, app mode, and permissions |

