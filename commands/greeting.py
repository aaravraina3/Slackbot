"""
Greeting Command
================

This is an example command that shows how to create a simple greeting.
Use this as a template for creating new commands.

For new team members:
- Copy this file to create a new command
- Change the function name and command name
- Add your command logic
- Register it in the command handler
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def handle_greeting_command(user_name: str, user_id: str) -> Dict[str, Any]:
    """
    Handle the greeting command.
    
    This function creates a response for when someone uses a greeting command.
    
    Args:
        user_name: The name of the user who ran the command
        user_id: The Slack user ID
        
    Returns:
        Dict[str, Any]: Response data for Slack
    """
    logger.info(f"Greeting command executed by {user_name} ({user_id})")
    
    # Create a personalized greeting
    greeting_text = f"👋 Hello {user_name}! Welcome to the Generate BSCI Slackbot!"
    
    # Create the response
    response = {
        "response_type": "in_channel",  # Visible to everyone
        "text": greeting_text,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{greeting_text}*\n\nI'm here to help with Generate BSCI club activities. How can I assist you today?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Get Help"
                        },
                        "action_id": "help_button",
                        "value": "help"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Bot Info"
                        },
                        "action_id": "info_button",
                        "value": "info"
                    }
                ]
            }
        ]
    }
    
    return response

def get_greeting_message(user_name: str = "there") -> str:
    """
    Get a simple greeting message.
    
    Args:
        user_name: The name of the user (default: "there")
        
    Returns:
        str: A greeting message
    """
    greetings = [
        f"👋 Hello {user_name}!",
        f"🤖 Greetings {user_name}!",
        f"👋 Hey there {user_name}!",
        f"🤖 Hi {user_name}! Nice to meet you!",
        f"👋 Welcome {user_name}!"
    ]
    
    # For now, just return the first one
    # You could make this random if you want
    return greetings[0]
