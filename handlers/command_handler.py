"""
Command Handler
===============

This file handles slash commands for the bot.
Slash commands are special commands that start with '/' in Slack.
For example: /hello, /help, /info

For new team members:
- Add new slash commands here
- Use the @app.command decorator to register commands
- Always provide helpful responses
- Handle errors gracefully
"""

import logging
from slack_bolt import App
from config.settings import bot_config

logger = logging.getLogger(__name__)

def setup_command_handlers(app: App):
    """
    Set up all slash command handlers for the bot.
    
    Args:
        app: The Slack Bolt app instance
    """
    logger.info("Setting up command handlers...")
    
    # Handle /hello command
    @app.command("/hello")
    def handle_hello_command(ack, respond, command):
        """
        Handle the /hello slash command.
        
        Args:
            ack: Function to acknowledge the command
            respond: Function to send a response
            command: The command data
        """
        try:
            # Always acknowledge the command first
            ack()
            
            user_id = command.get("user_id")
            user_name = command.get("user_name")
            channel_id = command.get("channel_id")
            
            logger.info(f"/hello command from user {user_name} ({user_id})")
            
            # Create a friendly response
            response = {
                "response_type": "in_channel",  # Visible to everyone in the channel
                "text": f"👋 Hello {user_name}! I'm {bot_config.bot_name}!",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"👋 *Hello {user_name}!*\n\nI'm {bot_config.bot_name} and I'm here to help with Generate BSCI club activities!"
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
                            }
                        ]
                    }
                ]
            }
            
            respond(response)
            
        except Exception as e:
            logger.error(f"Error handling /hello command: {e}")
            respond({"text": bot_config.error_message})
    
    # Handle /info command
    @app.command("/info")
    def handle_info_command(ack, respond, command):
        """
        Handle the /info slash command.
        
        Args:
            ack: Function to acknowledge the command
            respond: Function to send a response
            command: The command data
        """
        try:
            ack()
            
            user_name = command.get("user_name")
            
            logger.info(f"/info command from user {user_name}")
            
            # Get bot information
            bot_info = app.client.auth_test()
            bot_user_id = bot_info.get("user_id")
            
            response = {
                "response_type": "ephemeral",  # Only visible to the user who ran the command
                "text": f"🤖 Bot Information",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{bot_config.bot_name}*\n\n"
                                   f"• *Bot ID:* {bot_user_id}\n"
                                   f"• *Version:* 1.0.0\n"
                                   f"• *Status:* 🟢 Online\n"
                                   f"• *Purpose:* Generate BSCI Club Assistant\n\n"
                                   f"*Available Commands:*\n"
                                   f"• `/hello` - Say hello to the bot\n"
                                   f"• `/info` - Get bot information\n"
                                   f"• `/help` - Show help message\n"
                                   f"• `/ping` - Test bot response"
                        }
                    }
                ]
            }
            
            respond(response)
            
        except Exception as e:
            logger.error(f"Error handling /info command: {e}")
            respond({"text": bot_config.error_message})
    
    # Handle /help command
    @app.command("/help")
    def handle_help_command(ack, respond, command):
        """
        Handle the /help slash command.
        
        Args:
            ack: Function to acknowledge the command
            respond: Function to send a response
            command: The command data
        """
        try:
            ack()
            
            user_name = command.get("user_name")
            
            logger.info(f"/help command from user {user_name}")
            
            response = {
                "response_type": "ephemeral",
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
            logger.error(f"Error handling /help command: {e}")
            respond({"text": bot_config.error_message})
    
    # Handle /ping command
    @app.command("/ping")
    def handle_ping_command(ack, respond, command):
        """
        Handle the /ping slash command for testing.
        
        Args:
            ack: Function to acknowledge the command
            respond: Function to send a response
            command: The command data
        """
        try:
            ack()
            
            user_name = command.get("user_name")
            
            logger.info(f"/ping command from user {user_name}")
            
            response = {
                "response_type": "in_channel",
                "text": f"🏓 Pong! Bot is responding to {user_name}!"
            }
            
            respond(response)
            
        except Exception as e:
            logger.error(f"Error handling /ping command: {e}")
            respond({"text": bot_config.error_message})
    
    # Handle /status command
    @app.command("/status")
    def handle_status_command(ack, respond, command):
        """
        Handle the /status slash command.
        
        Args:
            ack: Function to acknowledge the command
            respond: Function to send a response
            command: The command data
        """
        try:
            ack()
            
            user_name = command.get("user_name")
            
            logger.info(f"/status command from user {user_name}")
            
            # Get some basic status information
            bot_info = app.client.auth_test()
            
            response = {
                "response_type": "ephemeral",
                "text": "📊 Bot Status",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{bot_config.bot_name} Status*\n\n"
                                   f"• *Status:* 🟢 Online and Healthy\n"
                                   f"• *Bot ID:* {bot_info.get('user_id', 'Unknown')}\n"
                                   f"• *Team:* {bot_info.get('team', 'Unknown')}\n"
                                   f"• *Development Mode:* {'Yes' if bot_config.is_development_mode() else 'No'}\n"
                                   f"• *Uptime:* All systems operational\n\n"
                                   f"Everything looks good! 👍"
                        }
                    }
                ]
            }
            
            respond(response)
            
        except Exception as e:
            logger.error(f"Error handling /status command: {e}")
            respond({"text": bot_config.error_message})
    
    logger.info("✅ Command handlers set up successfully")

def register_custom_command(app: App, command_name: str, handler_function):
    """
    Register a custom slash command.
    
    This is a helper function for adding new commands dynamically.
    
    Args:
        app: The Slack Bolt app instance
        command_name: The name of the command (without the /)
        handler_function: The function to handle the command
    """
    try:
        # Register the command with the app
        app.command(f"/{command_name}")(handler_function)
        logger.info(f"Registered custom command: /{command_name}")
    except Exception as e:
        logger.error(f"Error registering custom command /{command_name}: {e}")
