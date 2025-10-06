import sys

from bot.config import load_config
from bot.sheets import connect_to_sheets, get_roster, get_recent_selections, log_selection
from bot.selection import run_full_selection
from bot.slack import get_slack_client, lookup_user_by_email, send_dm
from bot.messages import render_initial


def main():
    cfg = load_config()
    service = connect_to_sheets(cfg.google_creds_path)

    roster = get_roster(service, cfg.google_sheets_id)
    recent = get_recent_selections(service, cfg.google_sheets_id, weeks=cfg.cooldown_weeks)

    selections = run_full_selection(roster, recent)
    client = get_slack_client()

    sent = 0
    for name, email in selections:
        user_id = lookup_user_by_email(client, email)
        if not user_id:
            # try alternate emails later if available; for now, skip
            print(f"[skip] No Slack user for {email}")
            continue
        message = render_initial(name=name, team=_team_for_email(roster, email))
        ok = send_dm(client, user_id, message)
        if ok:
            log_selection(service, cfg.google_sheets_id, email, name, _team_for_email(roster, email))
            sent += 1
            print(f"[ok] DM sent to {name} <{email}>")
        else:
            print(f"[fail] DM failed for {name} <{email}>")

    print(f"Done. Selected {len(selections)}, sent {sent} DMs.")


def _team_for_email(roster, email):
    email_lower = email.lower()
    for name, em, team, status in roster:
        if em.lower() == email_lower:
            return team
    return ""


if __name__ == "__main__":
    sys.exit(main())
