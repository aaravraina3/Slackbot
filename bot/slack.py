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
    """Look up a Slack user by their email address with smart fallbacks"""
    email_variations = [email]
    
    # If it's a northeastern email, also try husky version
    if '@northeastern.edu' in email:
        husky_email = email.replace('@northeastern.edu', '@husky.neu.edu')
        email_variations.append(husky_email)
        print(f"🔄 Will also try: {husky_email}")
    
    # If it's a husky email, also try northeastern version  
    elif '@husky.neu.edu' in email:
        northeastern_email = email.replace('@husky.neu.edu', '@northeastern.edu')
        email_variations.append(northeastern_email)
        print(f"🔄 Will also try: {northeastern_email}")
    
    # Try each email variation
    for email_attempt in email_variations:
        print(f"🔍 Trying: {email_attempt}")
        try:
            resp = client.users_lookupByEmail(email=email_attempt)
            user = resp.get("user")
            if user and not user.get("deleted", False):
                user_id = user.get("id")
                print(f"✅ Found with {email_attempt}: {user_id}")
                return user_id
        except SlackApiError as e:
            print(f"❌ Failed with {email_attempt}: {e}")
            continue
    
    print(f"❌ Could not find user with any email variation")
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
