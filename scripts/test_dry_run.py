import sys

from bot.config import load_config
from bot.sheets import connect_to_sheets, get_roster, get_recent_selections
from bot.selection import run_full_selection


def main():
    cfg = load_config()
    service = connect_to_sheets(cfg.google_creds_path)

    roster = get_roster(service, cfg.google_sheets_id)
    recent = get_recent_selections(service, cfg.google_sheets_id, weeks=cfg.cooldown_weeks)

    selections = run_full_selection(roster, recent)

    print("Dry run — would select:")
    for name, email in selections:
        team = _team_for_email(roster, email)
        print(f"- {name} <{email}> [{team}]")

    print(f"Total: {len(selections)}")


def _team_for_email(roster, email):
    email_lower = email.lower()
    for name, em, team, status in roster:
        if em.lower() == email_lower:
            return team
    return ""


if __name__ == "__main__":
    sys.exit(main())
