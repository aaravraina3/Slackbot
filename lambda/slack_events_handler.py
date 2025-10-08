#!/usr/bin/env python3
"""
AWS Lambda handler for Slack events (reactions, mentions, etc.)
This runs in real-time when Slack sends events
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

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for Slack events
    """
    print(f"🔔 Received event: {json.dumps(event, indent=2)}")
    
    try:
        # Handle different types of events
        if 'httpMethod' in event:
            # This is an API Gateway request
            return handle_api_gateway_event(event, context)
        elif 'source' in event and event['source'] == 'aws.events':
            # This is an EventBridge scheduled event
            return handle_scheduled_event(event, context)
        else:
            # Unknown event type
            print(f"❌ Unknown event type: {event}")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unknown event type'})
            }
            
    except Exception as e:
        print(f"❌ Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_api_gateway_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle API Gateway requests (Slack events)
    """
    print("🌐 Handling API Gateway event")
    
    # Parse the request body
    if event.get('isBase64Encoded'):
        import base64
        body = base64.b64decode(event['body']).decode('utf-8')
    else:
        body = event.get('body', '')
    
    print(f"📝 Request body: {body}")
    
    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        print("❌ Invalid JSON in request body")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON'})
        }
    
    # Handle different Slack event types
    if data.get('type') == 'url_verification':
        # Slack URL verification challenge
        return {
            'statusCode': 200,
            'body': data.get('challenge', '')
        }
    
    elif data.get('type') == 'event_callback':
        # Actual Slack event
        return handle_slack_event(data)
    
    else:
        print(f"❌ Unknown Slack event type: {data.get('type')}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Unknown event type'})
        }

def handle_slack_event(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle actual Slack events (reactions, messages, etc.)
    """
    event = data.get('event', {})
    event_type = event.get('type')
    
    print(f"📨 Handling Slack event: {event_type}")
    
    if event_type == 'reaction_added':
        return handle_reaction_added(event)
    else:
        print(f"ℹ️ Ignoring event type: {event_type}")
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'ignored'})
        }

def handle_reaction_added(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle when someone adds a reaction to a message
    """
    print("👍 Handling reaction added event")
    
    # Get reaction details
    reaction = event.get('reaction', '')
    user_id = event.get('user', '')
    message_ts = event.get('item', {}).get('ts', '')
    channel_id = event.get('item', {}).get('channel', '')
    
    print(f"📊 Reaction: {reaction}, User: {user_id}, Message: {message_ts}")
    
    # Handle any reaction on bot messages (any emoji counts!)
    print(f"📨 Processing reaction: {reaction}")
    
    try:
        # Get the user's email from Slack
        client = get_slack_client()
        user_info = client.users_info(user=user_id)
        
        if not user_info['ok']:
            print(f"❌ Failed to get user info: {user_info}")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Failed to get user info'})
            }
        
        user_email = user_info['user']['profile'].get('email', '').lower()
        print(f"📧 User email: {user_email}")
        
        if not user_email:
            print("❌ No email found for user")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No email found'})
            }
        
        # Mark as completed in Google Sheets
        sheets_service = connect_to_sheets()
        success = mark_completed(sheets_service, user_email)
        
        if success:
            print(f"✅ Marked {user_email} as completed in sheets")
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'success', 'email': user_email})
            }
        else:
            print(f"❌ Failed to mark {user_email} as completed")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to update sheets'})
            }
            
    except Exception as e:
        print(f"❌ Error handling reaction: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_scheduled_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle scheduled events (weekly selection, reminders)
    """
    print("⏰ Handling scheduled event")
    
    # This would call the existing selection/reminder scripts
    # For now, just log that we received a scheduled event
    print(f"📅 Scheduled event: {event}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'scheduled_event_received'})
    }
