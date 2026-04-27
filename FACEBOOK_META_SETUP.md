# Facebook / Meta Setup For This Instagram Bot

Use this checklist for each new business customer.

## 1. Instagram Account Requirements

- The Instagram account must be Professional: Business or Creator.
- You must be able to log in to the Instagram account.
- For production, the business should have a real privacy policy URL.

## 2. Create The Meta Developer App

Go to:

```text
https://developers.facebook.com/apps/
```

Create a new app for the customer. Choose the Instagram messaging/content use case when Meta asks for the app type or use case.

Add or enable the Instagram product/API flow that supports Instagram Login, Messaging, and Comments.

## 3. Add Permissions

The exact names shown by Meta can change, but this bot needs permissions for:

```text
instagram_business_basic
instagram_business_manage_messages
instagram_manage_comments
```

If Meta shows newer equivalent names, choose the matching Instagram basic profile, message management, and comment management permissions.

## 4. Add The Instagram Account

In the Meta app, open the Instagram API setup area and add the customer Instagram account.

If Meta shows `Insufficient Developer Role`:

1. Go to `App roles -> Roles`.
2. Add the Instagram account as an `Instagram Tester`.
3. Log in to Instagram as that account.
4. Open `https://www.instagram.com/accounts/manage_access/`.
5. Accept the tester invite.
6. Retry adding the account in Meta Developers.

## 5. Generate Token And Account ID

Generate the Instagram access token from the Meta app after the account is connected.

Save these values privately:

```text
ACCESS_TOKEN
INSTAGRAM_ACCOUNT_ID
```

Do not put real tokens in GitHub, README files, screenshots, or chat.

## 6. Deploy The Bot

Deploy this repo to Render as a Web Service.

Use:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn main:app
```

Add these Render environment variables:

```text
ACCESS_TOKEN=...
DEEPSEEK_API_KEY=...
DEEPSEEK_MODEL=deepseek-v4-flash
INSTAGRAM_ACCOUNT_ID=...
VERIFY_TOKEN=...
BRAND_NAME=...
WEBSITE_URL=...
BUSINESS_CONTEXT=...
```

`BUSINESS_CONTEXT` is what makes the same code work for a new business. Include services, products, location, working hours, pricing guidance, qualification questions, and the preferred call to action.

## 7. Configure Webhook In Meta

After Render is live, use:

```text
Callback URL: https://your-render-service.onrender.com/webhook
Verify Token: the same value as VERIFY_TOKEN in Render
```

Click `Verify and save`.

You can test verification in a browser:

```text
https://your-render-service.onrender.com/webhook?hub.mode=subscribe&hub.verify_token=YOUR_VERIFY_TOKEN&hub.challenge=test123
```

Expected response:

```text
test123
```

## 8. Subscribe Events

Turn on webhook subscriptions for the connected Instagram account.

Subscribe to:

```text
messages
comments
```

The bot ignores read receipts, message edits, deliveries, postbacks, echo messages, and its own comments.

## 9. Test

- Send a DM from a different Instagram account.
- Comment from a different Instagram account on a post.
- Watch Render logs for `POST /webhook`, `DeepSeek response`, and Instagram send/reply status.

If the Meta app is not live yet, add the sender Instagram account as a tester and accept the invite before testing.

## 10. Go Live

For customer production use:

- Add a privacy policy URL in Meta app settings.
- Complete any required business verification or app review Meta requests.
- Switch the app to live mode when approved.
- Refresh or rotate Instagram tokens when they expire.
