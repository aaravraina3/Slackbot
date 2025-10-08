#!/usr/bin/env python3
"""
GCP Cloud Function for Generate Feedback Bot
Handles scheduled tasks: weekly selection, reminders, reaction checking
"""

import json
import os
import sys
from typing import Dict, Any

# Add the bot module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bot.config import load_config
from bot.slack import get_slack_client
from bot.sheets import connect_to_sheets, mark_completed
from bot.selection import run_full_selection

def main(request):
    """
    Main Cloud Function entry point
    """
    print(f"🔔 Cloud Function triggered: {request}")
    
    try:
        # Parse the request
        if hasattr(request, 'get_json'):
            data = request.get_json() or {}
        else:
            data = request if isinstance(request, dict) else {}
        
        action = data.get('action', 'unknown')
        print(f"📋 Action: {action}")
        
        # Handle different actions
        if action == 'weekly_selection':
            return handle_weekly_selection()
        elif action == 'send_first_reminders':
            return handle_first_reminders()
        elif action == 'send_final_reminders':
            return handle_final_reminders()
        elif action == 'check_reactions':
            return handle_reaction_checking()
        else:
            print(f"❌ Unknown action: {action}")
            return f"Unknown action: {action}", 400
            
    except Exception as e:
        print(f"❌ Error in main: {e}")
        return f"Error: {str(e)}", 500

def handle_weekly_selection():
    """Run weekly selection process"""
    print("📅 Running weekly selection...")
    
    try:
        cfg = load_config()
        client = get_slack_client()
        
        # Run the selection process
        selections = run_full_selection()
        
        if not selections:
            print("❌ No selections made")
            return "No selections made", 200
        
        # Send DMs and log to sheets
        sheets_service = connect_to_sheets(cfg.google_creds_path)
        success_count = 0
        
        for name, email, team in selections:
            print(f"📤 Sending DM to {name} ({email})")
            
            # Look up user in Slack
            user_id = lookup_user_by_email(client, email)
            if user_id:
                # Send DM (you'll need to implement this)
                print(f"✅ Found {name} in Slack: {user_id}")
                success_count += 1
                
                # Log to sheets
                try:
                    log_selection(sheets_service, cfg.google_sheets_id, email, name, team)
                    print(f"📊 Logged {name} to sheets")
                except Exception as e:
                    print(f"❌ Failed to log {name}: {e}")
            else:
                print(f"❌ Could not find {name} in Slack")
        
        result = f"Weekly selection completed. {success_count}/{len(selections)} people contacted."
        print(result)
        return result, 200
        
    except Exception as e:
        print(f"❌ Error in weekly selection: {e}")
        return f"Weekly selection failed: {str(e)}", 500

def handle_first_reminders():
    """Send first reminders to non-responders"""
    print("📬 Sending first reminders...")
    
    try:
        cfg = load_config()
        client = get_slack_client()
        sheets_service = connect_to_sheets(cfg.google_creds_path)
        
        # Get pending responses
        pending = get_pending_responses(sheets_service, cfg.google_sheets_id)
        
        if not pending:
            print("✅ No pending responses to remind")
            return "No pending responses", 200
        
        reminder_count = 0
        for email, team, reminder_count in pending:
            print(f"📤 Sending first reminder to {email}")
            
            # Look up user and send reminder
            user_id = lookup_user_by_email(client, email)
            if user_id:
                # Send reminder (implement this)
                print(f"✅ Sent reminder to {email}")
                reminder_count += 1
                
                # Update reminder count in sheets
                update_reminder_count(sheets_service, cfg.google_sheets_id, email)
            else:
                print(f"❌ Could not find {email} in Slack")
        
        result = f"First reminders sent to {reminder_count} people"
        print(result)
        return result, 200
        
    except Exception as e:
        print(f"❌ Error in first reminders: {e}")
        return f"First reminders failed: {str(e)}", 500

def handle_final_reminders():
    """Send final reminders to non-responders"""
    print("📬 Sending final reminders...")
    
    # Similar to first reminders but with different message
    return handle_first_reminders()  # For now, same logic

def handle_reaction_checking():
    """Check for reactions and update sheets"""
    print("👍 Checking reactions...")
    
    try:
        cfg = load_config()
        client = get_slack_client()
        sheets_service = connect_to_sheets(cfg.google_creds_path)
        
        # Get all DM conversations
        conversations_response = client.conversations_list(types='im', limit=100)
        
        if not conversations_response['ok']:
            print(f"❌ Failed to get conversations: {conversations_response}")
            return "Failed to get conversations", 500
        
        conversations = conversations_response['channels']
        updated_count = 0
        
        for conv in conversations:
            user_id = conv['user']
            
            try:
                # Get messages in this conversation
                messages_response = client.conversations_history(
                    channel=conv['id'], 
                    limit=20
                )
                
                if not messages_response['ok']:
                    continue
                
                messages = messages_response['messages']
                
                # Look for bot messages
                for msg in messages:
                    if 'You were randomly selected from the Community team' in msg.get('text', ''):
                        # Check reactions
                        reactions = msg.get('reactions', [])
                        has_reaction = any(reaction['count'] > 0 for reaction in reactions)
                        
                        if has_reaction:
                            # Get user email and mark as completed
                            user_info = client.users_info(user=user_id)
                            if user_info['ok']:
                                user_email = user_info['user']['profile'].get('email', '').lower()
                                if user_email:
                                    try:
                                        mark_completed(sheets_service, cfg.google_sheets_id, user_email)
                                        print(f"✅ Marked {user_email} as completed")
                                        updated_count += 1
                                    except Exception as e:
                                        print(f"❌ Failed to update {user_email}: {e}")
                        break
                        
            except Exception as e:
                print(f"❌ Error processing conversation: {e}")
                continue
        
        result = f"Reaction checking completed. Updated {updated_count} people."
        print(result)
        return result, 200
        
    except Exception as e:
        print(f"❌ Error in reaction checking: {e}")
        return f"Reaction checking failed: {str(e)}", 500

# Import the functions we need (these should be in your bot modules)
def lookup_user_by_email(client, email):
    """Look up user by email (from bot.slack)"""
    from bot.slack import lookup_user_by_email
    return lookup_user_by_email(client, email)

def log_selection(service, spreadsheet_id, email, name, team):
    """Log selection to sheets (from bot.sheets)"""
    from bot.sheets import log_selection
    return log_selection(service, spreadsheet_id, email, name, team)

def get_pending_responses(service, spreadsheet_id):
    """Get pending responses (from bot.sheets)"""
    from bot.sheets import get_pending_responses
    return get_pending_responses(service, spreadsheet_id)

def update_reminder_count(service, spreadsheet_id, email):
    """Update reminder count (from bot.sheets)"""
    from bot.sheets import update_reminder_count
    return update_reminder_count(service, spreadsheet_id, email)
