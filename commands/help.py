"""
Help Command
============

This command provides help information to users.
It shows all available commands and how to use them.

For new team members:
- This command is already registered in the command handler
- You can modify the help text here
- Add new commands to the help message when you create them
"""

import logging
from config.settings import bot_config
from utils.helpers import create_help_blocks

logger = logging.getLogger(__name__)

def get_help_response() -> dict:
    """
    Get the help response for the bot.
    
    Returns:
        dict: Help response data
    """
    logger.info("Generating help response")
    
    # Get available commands from config
    commands = bot_config.get_commands()
    
    # Create help blocks
    help_blocks = create_help_blocks(commands)
    
    # Create the response
    response = {
        "response_type": "ephemeral",  # Only visible to the user
        "text": "🤖 Bot Help",
        "blocks": help_blocks
    }
    
    return response

def get_quick_help() -> str:
    """
    Get a quick help message for mentions.
    
    Returns:
        str: Quick help text
    """
    return f"""
🤖 **{bot_config.bot_name} Quick Help**

**Available Commands:**
• `/hello` - Say hello to the bot
• `/info` - Get bot information  
• `/help` - Show detailed help
• `/ping` - Test bot response
• `/status` - Check bot status

**Mention me** in a channel or **send me a DM** for assistance!

Need more help? Ask the development team! 💬
    """.strip()

def get_command_help(command_name: str) -> str:
    """
    Get help for a specific command.
    
    Args:
        command_name: The name of the command
        
    Returns:
        str: Command-specific help text
    """
    command_help = {
        "hello": "Say hello to the bot and get a friendly greeting.",
        "info": "Get detailed information about the bot, including version and status.",
        "help": "Show this help message with all available commands.",
        "ping": "Test if the bot is responding (useful for debugging).",
        "status": "Check the current status and health of the bot."
    }
    
    return command_help.get(command_name, f"No specific help available for /{command_name}")

def create_tutorial_blocks() -> list:
    """
    Create tutorial blocks for new users.
    
    Returns:
        list: List of tutorial blocks
    """
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🎓 Bot Tutorial"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*How to use the bot:*\n\n"
                        "1. **Slash Commands**: Type `/` followed by a command\n"
                        "2. **Mentions**: Use `@botname` to get my attention\n"
                        "3. **Direct Messages**: Send me a DM for private help\n"
                        "4. **Reactions**: React to my messages for quick responses"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Examples:*\n"
                        "• `/hello` - Get a greeting\n"
                        "• `@bot help` - Ask for help\n"
                        "• Send me a DM with any question"
            }
        }
    ]
    
    return blocks
