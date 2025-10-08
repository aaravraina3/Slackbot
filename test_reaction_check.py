#!/usr/bin/env python3
"""
Test if we can check reactions on messages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.config import load_config
from bot.slack import get_slack_client

def check_reactions_on_message(client, channel_id, message_ts):
    """Check reactions on a specific message"""
    try:
        response = client.reactions_get(
            channel=channel_id,
            timestamp=message_ts
        )
        
        if response['ok']:
            reactions = response.get('message', {}).get('reactions', [])
            print(f"📊 Found {len(reactions)} reactions:")
            
            for reaction in reactions:
                emoji = reaction['name']
                count = reaction['count']
                users = reaction.get('users', [])
                print(f"  {emoji}: {count} reactions from {len(users)} users")
                if users:
                    print(f"    Users: {users}")
            
            return reactions
        else:
            print(f"❌ Failed to get reactions: {response}")
            return []
            
    except Exception as e:
        print(f"❌ Error checking reactions: {e}")
        return []

def main():
    cfg = load_config()
    client = get_slack_client()
    
    print("=== REACTION CHECK TEST ===")
    
    # We need to find a recent message from the bot
    # Let's try to get recent DMs
    try:
        # Get list of conversations (DMs)
        response = client.conversations_list(types="im", limit=10)
        
        if response['ok']:
            conversations = response['channels']
            print(f"📋 Found {len(conversations)} DM conversations")
            
            for conv in conversations:
                user_id = conv['user']
                print(f"\n🔍 Checking DM with user: {user_id}")
                
                # Get recent messages in this DM
                try:
                    msg_response = client.conversations_history(
                        channel=conv['id'], 
                        limit=5
                    )
                    
                    if msg_response['ok']:
                        messages = msg_response['messages']
                        print(f"  Found {len(messages)} recent messages")
                        
                        for msg in messages:
                            # Look for messages from our bot
                            if msg.get('bot_id') or msg.get('user') == 'U09C5AWNDA7':  # Our bot ID
                                print(f"  🤖 Found bot message: {msg.get('text', '')[:50]}...")
                                print(f"  📅 Timestamp: {msg['ts']}")
                                
                                # Check reactions on this message
                                reactions = check_reactions_on_message(
                                    client, 
                                    conv['id'], 
                                    msg['ts']
                                )
                                
                                if reactions:
                                    print("  ✅ Found reactions!")
                                else:
                                    print("  ❌ No reactions found")
                                
                                break  # Just check the first bot message
                        else:
                            print("  ❌ No bot messages found in this DM")
                    else:
                        print(f"  ❌ Failed to get messages: {msg_response}")
                        
                except Exception as e:
                    print(f"  ❌ Error getting messages: {e}")
        else:
            print(f"❌ Failed to get conversations: {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
