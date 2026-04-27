# Daily Lead Report Setup

This is the simple alternative to Google Sheets.

The bot detects when an Instagram DM contains useful lead or support details, then:

1. Logs a `LEAD_CAPTURED` line in Render logs.
2. Saves the captured details in a small local log file.
3. Shows today's captured leads at a private report URL.

## Render Environment Variables

Add:

```text
LEAD_LOG_ENABLED=true
LEADS_REPORT_TOKEN=make_a_private_random_report_token
LOCAL_TIMEZONE=Asia/Kolkata
```

Use a private random value for `LEADS_REPORT_TOKEN`, for example:

```text
btnl_leads_2026_private_92841
```

Do not share this token publicly.

## How To Check Today's Leads

Open this URL:

```text
https://your-render-service.onrender.com/leads/today?token=YOUR_LEADS_REPORT_TOKEN
```

The response shows:

```json
{
  "date": "2026-04-27",
  "timezone": "Asia/Kolkata",
  "count": 1,
  "leads": []
}
```

If `count` is `0`, the AI has not captured lead details today.

## Render Logs

You can also check Render logs and search for:

```text
LEAD_CAPTURED
```

Each matching line means the bot detected and saved a lead/support detail from a DM.

## Important Limitation

This is intentionally simple and does not use a database. Render's filesystem can reset during redeploys or restarts, so this is good for quick daily checks, not long-term CRM storage.

For permanent lead storage later, use Google Sheets, Airtable, a database, or email notifications.
