import json

from bot.config import load_config
from bot.sheets import connect_to_sheets, get_roster, get_recent_selections, get_pending_responses, log_selection, update_reminder_count
from bot.selection import run_full_selection
from bot.slack import get_slack_client, lookup_user_by_email, send_dm
from bot.messages import render_initial, render_first_reminder, render_final_reminder


def lambda_handler(event, context):
    cfg = load_config()
    service = connect_to_sheets(cfg.google_creds_path)
    client = get_slack_client()

    action = (event or {}).get("action", "select")

    try:
        if action == "select":
            roster = get_roster(service, cfg.google_sheets_id)
            recent = get_recent_selections(service, cfg.google_sheets_id, weeks=cfg.cooldown_weeks)
            selections = run_full_selection(roster, recent)
            sent = 0
            for name, email in selections:
                user_id = lookup_user_by_email(client, email)
                if not user_id:
                    continue
                team = _team_for_email(roster, email)
                if send_dm(client, user_id, render_initial(name, team)):
                    log_selection(service, cfg.google_sheets_id, email, name, team)
                    sent += 1
            return _ok({"processed": len(selections), "sent": sent})

        elif action == "remind":
            pending = get_pending_responses(service, cfg.google_sheets_id)
            sent = 0
            for email, team, count in pending:
                if count != 0:
                    continue
                user_id = lookup_user_by_email(client, email)
                if not user_id:
                    continue
                if send_dm(client, user_id, render_first_reminder(team)):
                    update_reminder_count(service, cfg.google_sheets_id, email)
                    sent += 1
            return _ok({"sent": sent})

        elif action == "final":
            pending = get_pending_responses(service, cfg.google_sheets_id)
            sent = 0
            for email, team, count in pending:
                if count != 1:
                    continue
                user_id = lookup_user_by_email(client, email)
                if not user_id:
                    continue
                if send_dm(client, user_id, render_final_reminder(team)):
                    update_reminder_count(service, cfg.google_sheets_id, email)
                    sent += 1
            return _ok({"sent": sent})

        else:
            return _error(400, f"Unknown action: {action}")

    except Exception as e:
        return _error(500, str(e))


def _team_for_email(roster, email):
    email_lower = email.lower()
    for name, em, team, status in roster:
        if em.lower() == email_lower:
            return team
    return ""


def _ok(body_dict):
    return {"statusCode": 200, "body": json.dumps(body_dict)}


def _error(code, message):
    return {"statusCode": code, "body": json.dumps({"error": message})}
