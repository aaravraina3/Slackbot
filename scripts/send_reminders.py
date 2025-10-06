import sys

from bot.config import load_config
from bot.sheets import connect_to_sheets, get_pending_responses, update_reminder_count
from bot.slack import get_slack_client, lookup_user_by_email, send_dm
from bot.messages import render_first_reminder, render_final_reminder


def main():
    cfg = load_config()
    service = connect_to_sheets(cfg.google_creds_path)
    client = get_slack_client()

    pending = get_pending_responses(service, cfg.google_sheets_id)

    sent = 0
    for email, team, count in pending:
        user_id = lookup_user_by_email(client, email)
        if not user_id:
            print(f"[skip] No Slack user for {email}")
            continue

        if count == 0:
            msg = render_first_reminder(team)
        elif count == 1:
            msg = render_final_reminder(team)
        else:
            print(f"[skip] Already sent two reminders to {email}")
            continue

        if send_dm(client, user_id, msg):
            update_reminder_count(service, cfg.google_sheets_id, email)
            sent += 1
            print(f"[ok] Reminder {count+1} sent to <{email}>")
        else:
            print(f"[fail] Reminder failed for <{email}>")

    print(f"Done. Sent {sent} reminders.")


if __name__ == "__main__":
    sys.exit(main())
