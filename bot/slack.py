import time
import ssl
from typing import Dict, List, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .config import load_config


def get_slack_client() -> WebClient:
    cfg = load_config()
    # Create SSL context that doesn't verify certificates (for development)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    return WebClient(token=cfg.slack_bot_token, ssl=ssl_context)


def lookup_user_by_email(client: WebClient, email: str) -> Optional[str]:
    try:
        resp = client.users_lookupByEmail(email=email)
        user = resp.get("user")
        if user and not user.get("deleted", False):
            return user.get("id")
        return None
    except SlackApiError as e:
        # user_not_found or other errors
        return None


def batch_lookup_users(client: WebClient, email_list: List[str]) -> Dict[str, Optional[str]]:
    mapping: Dict[str, Optional[str]] = {e: None for e in email_list}
    try:
        cursor = None
        while True:
            resp = client.users_list(cursor=cursor, limit=200)
            members = resp.get("members", [])
            for m in members:
                if m.get("deleted"):
                    continue
                profile = m.get("profile", {})
                mail = (profile.get("email") or "").lower()
                if mail in mapping:
                    mapping[mail] = m.get("id")
            cursor = resp.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break
    except SlackApiError:
        pass
    return mapping


def send_dm(client: WebClient, user_id: str, message: str) -> bool:
    try:
        client.chat_postMessage(channel=user_id, text=message)
        time.sleep(1.0)
        return True
    except SlackApiError:
        return False
