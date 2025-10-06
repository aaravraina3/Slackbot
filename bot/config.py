import os
from dataclasses import dataclass
from typing import Dict
from dotenv import load_dotenv

# Load env vars from .env if present
load_dotenv()

# Google Sheets ranges
ROSTER_RANGE = "Roster!A:D"
TRACKING_RANGE = "Tracking!A:F"
CONFIG_RANGE = "Config!A:B"

DEFAULT_COOLDOWN_WEEKS = 4

@dataclass
class BotConfig:
    slack_bot_token: str
    google_sheets_id: str
    google_creds_path: str
    cooldown_weeks: int
    form_url: str
    team_counts: Dict[str, int]


def load_config() -> BotConfig:
    slack_bot_token = os.getenv("SLACK_BOT_TOKEN", "")
    google_sheets_id = os.getenv("GOOGLE_SHEETS_ID", "")
    google_creds_path = os.getenv("GOOGLE_CREDS_PATH", "credentials.json")

    # Defaults per spec
    cooldown_weeks = DEFAULT_COOLDOWN_WEEKS
    form_url = "https://forms.gle/f9SyxU3MzenqkVie7"  # Your Generate feedback form
    team_counts = {
        "software": 3,
        "data": 3,
        "default": 1,
    }

    return BotConfig(
        slack_bot_token=slack_bot_token,
        google_sheets_id=google_sheets_id,
        google_creds_path=google_creds_path,
        cooldown_weeks=cooldown_weeks,
        form_url=form_url,
        team_counts=team_counts,
    )
