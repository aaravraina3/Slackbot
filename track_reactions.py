#!/usr/bin/env python3
"""
Track reactions to bot messages and update tracking sheet
"""

from bot.config import load_config
from bot.slack import get_slack_client
from bot.sheets import get_sheets_service, update_response_status
import time

def track_reactions():
    """Check for reactions on recent bot messages and update tracking"""
    cfg = load_config()
    client = get_slack_client()
    sheets_service = get_sheets_service()
    
    # Get recent selections from tracking sheet
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=cfg.google_sheets_id,
            range="Tracking!A:F"
        ).execute()
        
        rows = result.get('values', [])
        if len(rows) <= 1:  # Only headers
            print("No recent selections to track")
            return
            
        # Check each recent selection for reactions
        for row in rows[1:]:  # Skip header
            if len(row) < 6:
                continue
                
            timestamp, name, email, team, slack_id, status = row
            
            if status == "Completed":
                continue  # Already completed
                
            try:
                # Get message history for this user
                response = client.conversations_history(
                    channel=slack_id,
                    limit=10
                )
                
                messages = response.get('messages', [])
                bot_messages = [msg for msg in messages if msg.get('bot_id')]
                
                # Check if any bot message has reactions
                for msg in bot_messages:
                    if 'reactions' in msg:
                        print(f"✅ {name} reacted to bot message!")
                        # Update status to completed
                        update_response_status(sheets_service, cfg.google_sheets_id, email, "Completed")
                        break
                        
            except Exception as e:
                print(f"Error checking reactions for {name}: {e}")
                
    except Exception as e:
        print(f"Error tracking reactions: {e}")

if __name__ == "__main__":
    track_reactions()
