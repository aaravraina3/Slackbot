#!/usr/bin/env python3
"""
Check for reactions on bot messages and update tracking
"""

from bot.config import load_config
from bot.slack import get_slack_client
from bot.sheets import connect_to_sheets, mark_completed
import time

def check_reactions():
    """Check for reactions on recent bot messages"""
    cfg = load_config()
    client = get_slack_client()
    sheets_service = connect_to_sheets(cfg.google_creds_path)
    
    print("🔍 Checking for reactions on bot messages...")
    
    try:
        # Get recent selections from tracking sheet
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=cfg.google_sheets_id,
            range="Tracking!A:F"
        ).execute()
        
        rows = result.get('values', [])
        if len(rows) <= 1:
            print("No recent selections to check")
            return
            
        updated_count = 0
        
        # Check each recent selection for reactions
        for i, row in enumerate(rows[1:], 1):  # Skip header
            if len(row) < 6:
                continue
                
            timestamp, name, email, team, slack_id, status = row
            
            if status == "Completed":
                continue  # Already completed
                
            print(f"Checking {name} ({email})...")
            
            try:
                # Get recent DM history for this user
                response = client.conversations_history(
                    channel=slack_id,
                    limit=20  # Check last 20 messages
                )
                
                messages = response.get('messages', [])
                
                # Look for bot messages with reactions
                for msg in messages:
                    # Check if this is a bot message (has bot_id)
                    if msg.get('bot_id') and 'reactions' in msg:
                        print(f"  ✅ Found reaction on bot message!")
                        
                        # Update status to completed
                        try:
                            mark_completed(sheets_service, cfg.google_sheets_id, email)
                            print(f"  ✅ Updated {name} to Completed")
                            updated_count += 1
                        except Exception as e:
                            print(f"  ❌ Failed to update {name}: {e}")
                        break
                        
            except Exception as e:
                print(f"  ❌ Error checking {name}: {e}")
                
        print(f"\n📊 Updated {updated_count} people to Completed status")
        
    except Exception as e:
        print(f"Error checking reactions: {e}")

def test_reaction_check():
    """Test reaction checking with a specific user"""
    cfg = load_config()
    client = get_slack_client()
    
    # Test with Aarav
    aarav_slack_id = "U096X0362RM"
    
    print(f"🔍 Testing reaction check for Aarav...")
    
    try:
        response = client.conversations_history(
            channel=aarav_slack_id,
            limit=10
        )
        
        messages = response.get('messages', [])
        print(f"Found {len(messages)} recent messages")
        
        for i, msg in enumerate(messages):
            print(f"\nMessage {i+1}:")
            print(f"  Bot ID: {msg.get('bot_id', 'None')}")
            print(f"  Text: {msg.get('text', 'No text')[:100]}...")
            print(f"  Reactions: {msg.get('reactions', 'None')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_reaction_check()
    else:
        check_reactions()
