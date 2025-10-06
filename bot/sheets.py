import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config import ROSTER_RANGE, TRACKING_RANGE

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


def connect_to_sheets(creds_path: str):
    try:
        credentials = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        service = build("sheets", "v4", credentials=credentials)
        return service
    except Exception as e:
        raise RuntimeError(f"Failed to authenticate with Google Sheets: {e}")


def _retry_call(func, *args, retries: int = 3, delay_sec: float = 1.5, **kwargs):
    last_err = None
    for _ in range(retries):
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            last_err = e
            time.sleep(delay_sec)
        except Exception as e:
            last_err = e
            time.sleep(delay_sec)
    if last_err:
        raise last_err


def get_roster(service, spreadsheet_id: str) -> List[List[str]]:
    resp = _retry_call(
        service.spreadsheets().values().get,
        spreadsheetId=spreadsheet_id,
        range=ROSTER_RANGE,
    ).execute()
    values = resp.get("values", [])
    if not values:
        return []

    # Skip header
    rows = values[1:]

    result: List[List[str]] = []
    for row in rows:
        # Ensure indices exist: A=name, B=email, C=team, D=status
        name = row[0].strip() if len(row) > 0 else ""
        email = row[1].strip() if len(row) > 1 else ""
        team = (row[2].strip() if len(row) > 2 else "").lower()
        status = row[3].strip() if len(row) > 3 else ""
        if status == "Active":
            result.append([name, email, team, status])
    return result


def get_recent_selections(service, spreadsheet_id: str, weeks: int = 4) -> List[str]:
    resp = _retry_call(
        service.spreadsheets().values().get,
        spreadsheetId=spreadsheet_id,
        range=TRACKING_RANGE,
    ).execute()
    values = resp.get("values", [])
    if not values:
        return []
    rows = values[1:]

    cutoff_date = datetime.utcnow().date() - timedelta(weeks=weeks)
    recent_emails: List[str] = []
    for row in rows:
        # A=email, B=team, C=date_selected
        if len(row) < 3:
            continue
        email = row[0].strip()
        date_str = row[2].strip()
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            if dt >= cutoff_date:
                recent_emails.append(email)
        except Exception:
            continue
    return recent_emails


def _week_start(date_obj) -> datetime:
    # Monday as the start of the week
    return date_obj - timedelta(days=date_obj.weekday())


def get_pending_responses(service, spreadsheet_id: str) -> List[Tuple[str, str, int]]:
    resp = _retry_call(
        service.spreadsheets().values().get,
        spreadsheetId=spreadsheet_id,
        range=TRACKING_RANGE,
    ).execute()
    values = resp.get("values", [])
    if not values:
        return []
    rows = values[1:]

    today = datetime.utcnow().date()
    start_of_week = _week_start(today)

    pending: List[Tuple[str, str, int]] = []
    for row in rows:
        # A=email, B=team, C=date_selected, D=form_completed, E=reminders_sent
        if len(row) < 5:
            continue
        email = row[0].strip()
        team = row[1].strip().lower()
        date_str = row[2].strip()
        completed = row[3].strip().upper() == "TRUE"
        reminders_sent = int(row[4]) if row[4].isdigit() else 0
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            if _week_start(dt) == start_of_week and not completed:
                pending.append((email, team, reminders_sent))
        except Exception:
            continue
    return pending


def log_selection(service, spreadsheet_id: str, email: str, name: str, team: str) -> None:
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    new_row = [email, team, today_str, "FALSE", 0, ""]
    _retry_call(
        service.spreadsheets().values().append,
        spreadsheetId=spreadsheet_id,
        range=TRACKING_RANGE,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [new_row]},
    ).execute()


def update_reminder_count(service, spreadsheet_id: str, email: str) -> None:
    # Read all rows to locate the row for this week and email, then update column E
    resp = _retry_call(
        service.spreadsheets().values().get,
        spreadsheetId=spreadsheet_id,
        range=TRACKING_RANGE,
    ).execute()
    values = resp.get("values", [])
    if not values:
        return

    rows = values[1:]
    today = datetime.utcnow().date()
    start_of_week = _week_start(today)

    for idx, row in enumerate(rows, start=2):  # account for header row at line 1
        if len(row) < 5:
            continue
        row_email = row[0].strip()
        date_str = row[2].strip() if len(row) > 2 else ""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            continue
        if row_email == email and _week_start(dt) == start_of_week:
            current = row[4]
            count = int(current) if str(current).isdigit() else 0
            count += 1
            rng = f"Tracking!E{idx}:E{idx}"
            _retry_call(
                service.spreadsheets().values().update,
                spreadsheetId=spreadsheet_id,
                range=rng,
                valueInputOption="USER_ENTERED",
                body={"values": [[count]]},
            ).execute()
            return


def mark_completed(service, spreadsheet_id: str, email: str) -> None:
    # Find this week's row by email and set D=TRUE, F=today
    resp = _retry_call(
        service.spreadsheets().values().get,
        spreadsheetId=spreadsheet_id,
        range=TRACKING_RANGE,
    ).execute()
    values = resp.get("values", [])
    if not values:
        return

    rows = values[1:]
    today = datetime.utcnow().date()
    start_of_week = _week_start(today)
    today_str = today.strftime("%Y-%m-%d")

    for idx, row in enumerate(rows, start=2):
        if len(row) < 6:
            continue
        row_email = row[0].strip()
        date_str = row[2].strip() if len(row) > 2 else ""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            continue
        if row_email == email and _week_start(dt) == start_of_week:
            rng_completed = f"Tracking!D{idx}:D{idx}"
            rng_date = f"Tracking!F{idx}:F{idx}"
            _retry_call(
                service.spreadsheets().values().batchUpdate,
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": rng_completed, "values": [["TRUE"]]},
                        {"range": rng_date, "values": [[today_str]]},
                    ],
                },
            ).execute()
            return
