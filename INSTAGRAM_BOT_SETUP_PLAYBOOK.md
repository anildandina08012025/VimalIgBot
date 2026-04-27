# Instagram AI Bot Setup Playbook

Use this file as the reusable guide for setting up the same Instagram AI bot for another business. Give this file to an AI assistant and ask it to help you follow the checklist for the new business.

## What This Bot Does

- Receives Instagram DMs through Meta webhooks.
- Receives Instagram post comments through Meta webhooks.
- Sends each valid message/comment to an AI model.
- Replies back through the Instagram Graph API.
- Runs on Render using a GitHub repo.

Current codebase uses:

| Area | Tool |
|------|------|
| Backend | Python + Flask |
| Hosting | Render Web Service |
| Source control | GitHub |
| Instagram API | Meta Instagram API |
| AI | DeepSeek API |

## Files In The Repo

| File | Purpose |
|------|---------|
| `main.py` | Flask webhook server and bot logic |
| `requirements.txt` | Python packages |
| `render.yaml` | Render build/start config |
| `.gitignore` | Prevents secrets/logs/cache from being committed |
| `instagram_bot_README.md` | Current project notes |
| `instagram_bot_SKILL.md` | Skill/report notes |

Never commit token files such as `Instadetailstemp.txt`.

## New Business Setup Checklist

### 1. Prepare Instagram Account

The Instagram account must be a Professional account.

In Instagram:

```text
Profile -> Settings -> Account type and tools -> Switch to professional account
```

Use Business or Creator.

### 2. Create Meta Developer App

Go to:

```text
https://developers.facebook.com/apps/
```

Create an app with a clear name, for example:

```text
BusinessName Instagram Bot
```

Choose the use case:

```text
Manage messaging & content on Instagram
```

Add required permissions:

```text
instagram_business_basic
instagram_business_manage_messages
instagram_manage_comments
```

Some screens may also show:

```text
instagram_business_manage_comments
instagram_business_content_publish
instagram_business_manage_insights
```

Accept the permissions that match the use case.

### 3. Connect Instagram Account

In the Meta app:

```text
Use cases -> Customize -> API setup with Instagram login -> Generate access tokens -> Add account
```

If you get:

```text
Insufficient Developer Role
```

Fix:

1. Go to `App roles -> Roles`.
2. Add the Instagram account as `Instagram Tester`.
3. Login to that Instagram account.
4. Open:

```text
https://www.instagram.com/accounts/manage_access/
```

5. Click `Tester Invites`.
6. Accept the invite.
7. Retry `Add account`.

Also make sure the Instagram account is connected in Business Manager:

```text
Business Settings -> Accounts -> Instagram accounts -> Add
```

### 4. Generate Instagram Access Token

After the account is connected, click:

```text
Generate token
```

Copy:

```text
ACCESS_TOKEN
INSTAGRAM_ACCOUNT_ID
```

Store them only in a local temporary file or password manager. Do not commit them.

### 5. Create Or Update GitHub Repo

For a new business, use a fresh GitHub repo.

If the repo was cloned from someone else's project and GitHub blocks push because of old secrets, create a clean history:

```powershell
git checkout --orphan clean-main
git reset --mixed
git add .gitignore README.md main.py render.yaml requirements.txt instagram_bot_README.md instagram_bot_SKILL.md INSTAGRAM_BOT_SETUP_PLAYBOOK.md
git commit -m "Initial Instagram AI bot"
git branch -D main
git branch -m main
git push -u origin main
```

Only do this for a new repo or when you intentionally want to remove old history.

### 6. Deploy On Render

Create a new Render Web Service.

Use:

```text
Language: Python 3
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn main:app
```

Root Directory:

```text
leave blank
```

Add environment variables:

```text
ACCESS_TOKEN=instagram_access_token
DEEPSEEK_API_KEY=deepseek_api_key
DEEPSEEK_MODEL=deepseek-v4-flash
INSTAGRAM_ACCOUNT_ID=instagram_account_id
VERIFY_TOKEN=business_unique_verify_token
BRAND_NAME=Business Name
WEBSITE_URL=https://businesswebsite.com
BUSINESS_CONTEXT=Short but complete description of services, pricing, offer, target customers, and call-to-action.
```

Example `BUSINESS_CONTEXT`:

```text
Aivoro Private Limited helps businesses adopt practical AI solutions. Services include AI automation, Instagram and website chatbots, custom AI assistants, workflow automation, AI integrations for business tools, lead capture automation, customer support automation, and AI consulting for companies that want to use AI in daily operations.
```

### 7. Configure Meta Webhook

After Render is live, get the Render URL:

```text
https://your-render-service.onrender.com
```

Meta webhook callback URL:

```text
https://your-render-service.onrender.com/webhook
```

Verify token must exactly match Render:

```text
VERIFY_TOKEN
```

Click:

```text
Verify and save
```

Test in browser:

```text
https://your-render-service.onrender.com/webhook?hub.mode=subscribe&hub.verify_token=VERIFY_TOKEN&hub.challenge=test123
```

Expected response:

```text
test123
```

### 8. Turn On Webhook Subscription

In Step 2 / Generate access tokens, make sure:

```text
Webhook Subscription: On
```

for the connected Instagram account.

### 9. Set Up Instagram Business Login

For the redirect URL, use the Render base URL:

```text
https://your-render-service.onrender.com/
```

Do not use `/webhook` for business login redirect.

Webhook URL and redirect URL are different:

```text
Webhook callback: https://your-render-service.onrender.com/webhook
Business login redirect: https://your-render-service.onrender.com/
```

### 10. Publish App Or Use Testers

For testing, add sender accounts as Instagram testers:

```text
App roles -> Roles -> Add People -> Instagram Tester
```

Then accept the invite from:

```text
https://www.instagram.com/accounts/manage_access/
```

For live usage, add a privacy policy URL and publish the app if Meta requires it.

Privacy policy URL must be a real page, for example:

```text
https://businesswebsite.com/privacy-policy
```

## Testing Procedure

### Webhook Verification Test

Open:

```text
https://your-render-service.onrender.com/webhook?hub.mode=subscribe&hub.verify_token=VERIFY_TOKEN&hub.challenge=test123
```

Expected:

```text
test123
```

### DM Test

From a different Instagram account, send a DM to the connected business account.

Render logs should show:

```text
POST /webhook
Received: {...}
DeepSeek response: {...}
DM Reply sent: 200 - ...
```

### Comment Test

From a different Instagram account, comment on a post.

Render logs should show:

```text
POST /webhook
Received: {...}
New comment from @username: ...
Comment Reply sent: 200 - ...
```

## Problems We Faced And Fixes

### Problem: Git Clone Failed With `.git/config.lock`

Symptoms:

```text
could not write config file .git/config: Permission denied
```

Fix:

- Remove the failed partial `.git` directory.
- Retry clone with proper permissions.
- If needed, run the Git command outside sandbox/with approval.

### Problem: Virtualenv Created Without Pip

Symptoms:

```text
No module named pip
ensurepip PermissionError
```

Fix:

```powershell
.\.venv\Scripts\python.exe -m ensurepip --upgrade --default-pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If Temp directory permission fails, run with elevated permission.

### Problem: Instagram OAuth Says `Insufficient Developer Role`

Cause:

- Instagram account is not added as tester/developer for the Meta app.
- Or the wrong Instagram account is logged in.

Fix:

1. Add the Instagram username as `Instagram Tester`.
2. Accept invite at:

```text
https://www.instagram.com/accounts/manage_access/
```

3. Confirm Chrome is logged into the same Instagram account.
4. Retry `Add account`.

### Problem: Webhook Verification Works But No DM Event Arrives

Symptoms:

Render logs show only:

```text
GET /webhook?...challenge=test123
```

but no:

```text
POST /webhook
```

Fix:

- Send DM from a different Instagram account.
- Make sender account a tester if app is unpublished/development.
- Confirm webhook subscription is On.
- Confirm account is connected and token generated.
- Publish app if needed.

### Problem: Render Logs Show `Error: 'sender'`

Cause:

Instagram sent a `message_edit` webhook event. It does not include `sender`.

Fix:

Code must skip non-reply events:

```text
read
message_edit
delivery
postback
echo messages
events without sender/text
```

This has been fixed in `main.py`.

### Problem: Bot Does Not Reply But Webhook POST Arrives

Check Render logs.

If DeepSeek error:

```text
401/403
```

Fix:

- Rotate DeepSeek key.
- Update `DEEPSEEK_API_KEY` in Render.
- Confirm account has credits/access.

If Instagram send error:

```text
400/401
```

Fix:

- Regenerate Instagram token.
- Update `ACCESS_TOKEN` in Render.
- Confirm app has message/comment permissions.
- Confirm the token belongs to the connected Instagram account.

### Problem: GitHub Blocks Push Due To Secret

Symptoms:

```text
GH013: Repository rule violations found
Push cannot contain secrets
```

Cause:

Some earlier commit in history contains an API key or access token.

Fix:

- For a new repo, create clean orphan history.
- Never push token files.
- Add secrets file to `.gitignore`.
- Rotate any exposed keys.

### Problem: Render Free Instance Sleeps

Symptoms:

- First request after inactivity takes 50+ seconds.

Fix:

- Use paid Render plan, or
- Accept delay during testing, or
- Use an uptime ping service if acceptable for your use case.

## Security Rules

- Never paste long-lived tokens into public chat, GitHub, README, or screenshots.
- If a token is exposed, rotate it.
- Keep `Instadetailstemp.txt` ignored.
- Store real values only in Render environment variables or a password manager.

## Current Known Good Commands

Local setup:

```powershell
cd "d:\Projects\Instagram Bot"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Local run:

```powershell
$env:ACCESS_TOKEN="..."
$env:DEEPSEEK_API_KEY="..."
$env:DEEPSEEK_MODEL="deepseek-v4-flash"
$env:INSTAGRAM_ACCOUNT_ID="..."
$env:VERIFY_TOKEN="..."
$env:BRAND_NAME="Business Name"
$env:WEBSITE_URL="https://businesswebsite.com"
$env:BUSINESS_CONTEXT="Business services and offer..."

.\.venv\Scripts\python.exe main.py
```

Git push:

```powershell
git add .
git commit -m "Update Instagram bot"
git push
```

Render manual deploy:

```text
Manual Deploy -> Deploy latest commit
```

## Prompt To Give An AI Assistant Next Time

```text
Read INSTAGRAM_BOT_SETUP_PLAYBOOK.md and help me set up this Instagram AI bot for a new business. Guide me step by step through Meta Developer, Instagram tester setup, Render environment variables, webhook verification, and debugging Render logs. Do not let me commit secrets. If I show an error, match it against the Problems We Faced section and tell me the fix.
```

