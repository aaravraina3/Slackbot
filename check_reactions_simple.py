#!/usr/bin/env python3
"""
Simple reaction checker - run this periodically to update the sheet
This doesn't need real-time events, just checks reactions on known messages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.config import load_config
from bot.slack import get_slack_client
from bot.sheets import connect_to_sheets, mark_completed
from datetime import datetime

def check_reactions_and_update_sheet():
    """Check for reactions and update the tracking sheet"""
    cfg = load_config()
    client = get_slack_client()
    
    print("=== CHECKING REACTIONS AND UPDATING SHEET ===")
    
    # For now, we'll manually track which messages we sent
    # In a real implementation, we'd store message timestamps in the sheet
    
    # Get pending responses from the sheet
    try:
        sheets_service = connect_to_sheets()
        # This would get people who haven't completed yet
        # For now, just print what we'd do
        
        print("📋 Would check sheet for pending responses...")
        print("🔍 Would check reactions on their messages...")
        print("✅ Would mark completed if they reacted with 👍")
        
        # Example of what the logic would be:
        # 1. Get pending responses from sheet
        # 2. For each person, check if they reacted to their message
        # 3. If they reacted with 👍, mark them as completed
        
        print("\n💡 This script would:")
        print("   - Read 'Tracking' sheet for incomplete responses")
        print("   - Check reactions on their DM messages") 
        print("   - Update sheet when they react with 👍")
        print("   - Send reminders to non-responders")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_reactions_and_update_sheet()
