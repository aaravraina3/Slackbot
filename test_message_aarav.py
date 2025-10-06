#!/usr/bin/env python3
"""
Send test message just to Aarav Raina
"""

from bot.config import load_config
from bot.slack import get_slack_client, lookup_user_by_email, send_dm
from bot.messages import render_initial

def main():
    cfg = load_config()
    client = get_slack_client()
    
    # Your email from the roster
    your_email = "raina.aa@northeastern.edu"
    
    print(f"Looking up Slack user for {your_email}...")
    user_id = lookup_user_by_email(client, your_email)
    
    if not user_id:
        print("❌ Could not find your Slack user ID")
        return
    
    print(f"✅ Found your Slack ID: {user_id}")
    
    # Send test message
    message = render_initial("Aarav", "community internal insights")
    print(f"Sending message: {message}")
    
    success = send_dm(client, user_id, message)
    
    if success:
        print("✅ Test message sent to you!")
    else:
        print("❌ Failed to send message")

if __name__ == "__main__":
    main()
