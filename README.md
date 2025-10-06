# Generate Feedback Bot

Automated weekly Slack DMs for team feedback using Google Sheets as the datastore.

## Setup
1. Create `.env` with:
```
SLACK_BOT_TOKEN=xoxb-...
GOOGLE_SHEETS_ID=...
GOOGLE_CREDS_PATH=credentials.json
ENVIRONMENT=development
```
2. Put your Google service account JSON at `credentials.json` and share your Sheet with that service account.
3. Install deps: `pip install -r requirements.txt`

## Scripts
- `scripts/test_dry_run.py` — shows who would be selected (no DMs, no writes)
- `scripts/run_selection.py` — selects, DMs, logs to Tracking
- `scripts/send_reminders.py` — sends reminders and increments counts

## Lambda
- Use `lambda/handler.py` with event `{"action": "select"|"remind"|"final"}`
- Schedule with EventBridge: Mon 9am, Wed 2pm, Fri 3pm (EST)
