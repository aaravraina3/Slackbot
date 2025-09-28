"""
Event Handler
=============

This file handles Slack events like user joining channels,
reactions, file uploads, etc.

For new team members:
- Add new event handlers here
- Use the @app.event decorator to handle specific events
- Events are things that happen in Slack (user joins, messages, etc.)
"""

import logging
from slack_bolt import App
from config.settings import bot_config

logger = logging.getLogger(__name__)

def setup_event_handlers(app: App):
    """
    Set up all event handlers for the bot.
    
    Args:
        app: The Slack Bolt app instance
    """
    logger.info("Setting up event handlers...")
    
    # Handle user joining a channel
    @app.event("member_joined_channel")
    def handle_member_joined(event, say):
        """
        Handle when a user joins a channel.
        
        Args:
            event: The Slack event data
            say: Function to send a message
        """
        try:
            user_id = event.get("user")
            channel_id = event.get("channel")
            
            logger.info(f"User {user_id} joined channel {channel_id}")
            
            # Get user information
            user_info = app.client.users_info(user=user_id)
            user_name = user_info.get("user", {}).get("real_name", "New Member")
            
            # Send a welcome message (only if it's not a DM channel)
            if channel_id and not channel_id.startswith("D"):
                welcome_message = f"👋 Welcome to the channel, {user_name}! I'm {bot_config.bot_name}. Type `/help` to see what I can do!"
                say(text=welcome_message, channel=channel_id)
            
        except Exception as e:
            logger.error(f"Error handling member joined event: {e}")
    
    # Handle reactions to messages
    @app.event("reaction_added")
    def handle_reaction_added(event, say):
        """
        Handle when someone adds a reaction to a message.
        
        Args:
            event: The Slack event data
            say: Function to send a message
        """
        try:
            reaction = event.get("reaction")
            user_id = event.get("user")
            item = event.get("item", {})
            channel_id = item.get("channel")
            
            logger.info(f"Reaction '{reaction}' added by user {user_id}")
            
            # Respond to specific reactions
            if reaction == "wave":
                say(text="👋 I see you waving! Hello there!", channel=channel_id)
            elif reaction == "robot_face":
                say(text="🤖 Yes, I am a robot! Beep boop!", channel=channel_id)
            elif reaction == "question":
                say(text="❓ I see you have a question! How can I help?", channel=channel_id)
            
        except Exception as e:
            logger.error(f"Error handling reaction added event: {e}")
    
    # Handle file uploads
    @app.event("file_shared")
    def handle_file_shared(event, say):
        """
        Handle when someone shares a file.
        
        Args:
            event: The Slack event data
            say: Function to send a message
        """
        try:
            file_id = event.get("file_id")
            user_id = event.get("user_id")
            channel_id = event.get("channel_id")
            
            logger.info(f"File {file_id} shared by user {user_id}")
            
            # Get file information
            file_info = app.client.files_info(file=file_id)
            file_data = file_info.get("file", {})
            file_name = file_data.get("name", "Unknown file")
            file_type = file_data.get("filetype", "unknown")
            
            # Respond based on file type
            if file_type in ["jpg", "jpeg", "png", "gif"]:
                say(text=f"📸 Thanks for sharing the image '{file_name}'!", channel=channel_id)
            elif file_type in ["pdf", "doc", "docx"]:
                say(text=f"📄 Document '{file_name}' shared successfully!", channel=channel_id)
            else:
                say(text=f"📎 File '{file_name}' has been shared!", channel=channel_id)
            
        except Exception as e:
            logger.error(f"Error handling file shared event: {e}")
    
    # Handle button clicks (from interactive components)
    @app.action("help_button")
    def handle_help_button(ack, body, respond):
        """
        Handle when someone clicks the help button.
        
        Args:
            ack: Function to acknowledge the action
            body: The action body data
            respond: Function to send a response
        """
        try:
            ack()
            
            user_id = body.get("user", {}).get("id")
            
            logger.info(f"Help button clicked by user {user_id}")
            
            response = {
                "text": "🤖 Help Information",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": bot_config.help_message
                        }
                    }
                ]
            }
            
            respond(response)
            
        except Exception as e:
            logger.error(f"Error handling help button: {e}")
    
    # Handle when the bot is added to a channel
    @app.event("app_home_opened")
    def handle_app_home_opened(event, say):
        """
        Handle when someone opens the bot's app home.
        
        Args:
            event: The Slack event data
            say: Function to send a message
        """
        try:
            user_id = event.get("user")
            
            logger.info(f"App home opened by user {user_id}")
            
            # You could send a welcome message to the user's DM here
            # say(text=bot_config.welcome_message, channel=user_id)
            
        except Exception as e:
            logger.error(f"Error handling app home opened event: {e}")
    
    # Handle errors
    @app.error
    def handle_errors(error, body, logger):
        """
        Handle any errors that occur in the bot.
        
        Args:
            error: The error that occurred
            body: The request body
            logger: The logger instance
        """
        logger.error(f"Bot error: {error}")
        logger.error(f"Request body: {body}")
    
    logger.info("✅ Event handlers set up successfully")

def send_welcome_dm(app: App, user_id: str):
    """
    Send a welcome direct message to a new user.
    
    Args:
        app: The Slack Bolt app instance
        user_id: The Slack user ID to send the message to
    """
    try:
        app.client.chat_postMessage(
            channel=user_id,
            text=bot_config.welcome_message
        )
        logger.info(f"Welcome DM sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending welcome DM: {e}")

def send_channel_notification(app: App, channel_id: str, message: str):
    """
    Send a notification message to a specific channel.
    
    Args:
        app: The Slack Bolt app instance
        channel_id: The channel to send the message to
        message: The message to send
    """
    try:
        app.client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        logger.info(f"Notification sent to channel {channel_id}")
    except Exception as e:
        logger.error(f"Error sending channel notification: {e}")
