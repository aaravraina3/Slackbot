#!/usr/bin/env python3
"""
Send test message to Neha Jha
"""

from bot.config import load_config
from bot.slack import get_slack_client, lookup_user_by_email, send_dm
from bot.messages import render_initial

def main():
    cfg = load_config()
    client = get_slack_client()
    
    # Neha Jha's email from the roster - try personal email
    neha_email = "nehajha2004@gmail.com"
    
    print(f"Looking up Slack user for {neha_email}...")
    user_id = lookup_user_by_email(client, neha_email)
    
    if not user_id:
        print("❌ Could not find Neha's Slack user ID")
        return
    
    print(f"✅ Found Neha's Slack ID: {user_id}")
    
    # Send test message
    message = render_initial("Neha", "community internal insights")
    print(f"Sending message: {message}")
    
    success = send_dm(client, user_id, message)
    
    if success:
        print("✅ Test message sent to Neha!")
    else:
        print("❌ Failed to send message")

if __name__ == "__main__":
    main()
