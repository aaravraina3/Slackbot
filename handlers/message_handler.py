"""
Message Handler
===============

This file handles all incoming messages to the bot.
When someone sends a message that mentions the bot or sends a DM,
this handler processes the message and responds appropriately.

For new team members:
- Add new message handling logic here
- Use the @app.message decorator to handle specific message patterns
- Always handle errors gracefully
"""

import logging
from slack_bolt import App
from config.settings import bot_config

logger = logging.getLogger(__name__)

def setup_message_handlers(app: App):
    """
    Set up all message handlers for the bot.
    
    Args:
        app: The Slack Bolt app instance
    """
    logger.info("Setting up message handlers...")
    
    # Handle direct mentions of the bot
    @app.event("app_mention")
    def handle_app_mention(event, say):
        """
        Handle when someone mentions the bot in a channel.
        
        Args:
            event: The Slack event data
            say: Function to send a message back
        """
        try:
            # Get the user who mentioned the bot
            user_id = event.get("user")
            channel = event.get("channel")
            text = event.get("text", "")
            
            logger.info(f"Bot mentioned by user {user_id} in channel {channel}")
            
            # Remove the bot mention from the text to get the actual message
            bot_mention = f"<@{app.client.auth_test()['user_id']}>"
            message_text = text.replace(bot_mention, "").strip()
            
            # Respond based on the message content
            if not message_text:
                # Just a mention without any message
                response = f"👋 Hello! I'm {bot_config.bot_name}. How can I help you today?"
            elif "hello" in message_text.lower():
                response = f"👋 Hello there! Nice to meet you!"
            elif "help" in message_text.lower():
                response = bot_config.help_message
            elif "status" in message_text.lower():
                response = "🟢 Bot is running and healthy! All systems operational."
            else:
                response = f"🤔 I heard you mention me! You said: '{message_text}'\n\nType 'help' if you need assistance!"
            
            # Send the response
            say(text=response, channel=channel)
            
        except Exception as e:
            logger.error(f"Error handling app mention: {e}")
            say(text=bot_config.error_message, channel=event.get("channel"))
    
    # Handle direct messages to the bot
    @app.event("message")
    def handle_direct_message(event, say):
        """
        Handle direct messages sent to the bot.
        
        Args:
            event: The Slack event data
            say: Function to send a message back
        """
        try:
            # Check if this is a direct message (channel type is 'im')
            if event.get("channel_type") != "im":
                return  # Not a direct message, ignore
            
            # Check if the message is from a bot (avoid responding to other bots)
            if event.get("bot_id"):
                return
            
            user_id = event.get("user")
            channel = event.get("channel")
            text = event.get("text", "")
            
            logger.info(f"Direct message from user {user_id}: {text}")
            
            # Process the message and respond
            if "hello" in text.lower():
                response = f"👋 Hello! Thanks for messaging me directly!"
            elif "help" in text.lower():
                response = bot_config.help_message
            elif "ping" in text.lower():
                response = "🏓 Pong! Bot is responding."
            else:
                response = f"🤖 Thanks for your message: '{text}'\n\nI'm here to help! Type 'help' for available commands."
            
            say(text=response, channel=channel)
            
        except Exception as e:
            logger.error(f"Error handling direct message: {e}")
            say(text=bot_config.error_message, channel=event.get("channel"))
    
    # Handle messages containing specific keywords
    @app.message("hello")
    def handle_hello_message(message, say):
        """
        Handle messages that contain the word 'hello'.
        
        Args:
            message: The message data
            say: Function to send a message back
        """
        try:
            user_id = message.get("user")
            channel = message.get("channel")
            
            logger.info(f"Hello message from user {user_id}")
            
            response = f"👋 Hello! I'm {bot_config.bot_name}. How can I help you today?"
            say(text=response, channel=channel)
            
        except Exception as e:
            logger.error(f"Error handling hello message: {e}")
    
    # Handle messages with questions
    @app.message("?")
    def handle_question_message(message, say):
        """
        Handle messages that contain question marks.
        
        Args:
            message: The message data
            say: Function to send a message back
        """
        try:
            user_id = message.get("user")
            channel = message.get("channel")
            text = message.get("text", "")
            
            logger.info(f"Question from user {user_id}: {text}")
            
            response = "🤔 I see you have a question! I'm still learning, but I'll do my best to help. What would you like to know?"
            say(text=response, channel=channel)
            
        except Exception as e:
            logger.error(f"Error handling question message: {e}")
    
    logger.info("✅ Message handlers set up successfully")

def get_user_info(app: App, user_id: str) -> dict:
    """
    Get information about a user.
    
    Args:
        app: The Slack Bolt app instance
        user_id: The Slack user ID
        
    Returns:
        dict: User information
    """
    try:
        result = app.client.users_info(user=user_id)
        return result.get("user", {})
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        return {}
