"""
Bot Configuration Settings
=========================

This file contains all the configuration settings for the bot.
It's a good place to put settings that might change between
development and production environments.

For new team members:
- Add new settings here instead of hardcoding them in other files
- Use environment variables for sensitive data
- Keep all bot configuration in one place
"""

import os
from typing import Dict, Any

class BotConfig:
    """
    Bot configuration class.
    
    This class holds all the configuration settings for the bot.
    It reads from environment variables and provides default values.
    """
    
    def __init__(self):
        """Initialize bot configuration from environment variables."""
        
        # Bot identity
        self.bot_name = os.getenv("BOT_NAME", "Generate BSCI Bot")
        self.bot_emoji = os.getenv("BOT_EMOJI", ":robot_face:")
        
        # Slack tokens (required)
        self.slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.slack_app_token = os.getenv("SLACK_APP_TOKEN")
        self.signing_secret = os.getenv("SIGNING_SECRET")
        
        # Default channel for announcements
        self.default_channel = os.getenv("DEFAULT_CHANNEL", "#general")
        
        # Logging configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.development_mode = os.getenv("DEVELOPMENT_MODE", "true").lower() == "true"
        
        # Database configuration (optional)
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///bot_database.db")
        
        # Bot behavior settings
        self.max_message_length = 4000  # Slack's message limit
        self.command_prefix = "/"        # Prefix for slash commands
        self.mention_prefix = "<@"       # How the bot gets mentioned
        
        # Response templates
        self.help_message = self._get_help_message()
        self.welcome_message = self._get_welcome_message()
        self.error_message = "❌ Sorry, something went wrong. Please try again later."
    
    def _get_help_message(self) -> str:
        """Get the help message that users see when they ask for help."""
        return f"""
🤖 **{self.bot_name} Help**

Here are the commands I understand:

**Slash Commands:**
• `/hello` - Say hello to the bot
• `/info` - Get information about the bot
• `/help` - Show this help message

**Mentions:**
• Mention me (@{self.bot_name}) and I'll respond!

**Direct Messages:**
• Send me a DM and I'll respond directly

Need more help? Ask the development team!
        """.strip()
    
    def _get_welcome_message(self) -> str:
        """Get the welcome message for new users."""
        return f"""
👋 Welcome to the {self.bot_name}!

I'm here to help with Generate BSCI club activities.
Type `/help` to see what I can do, or just mention me in a channel!

Happy to help! {self.bot_emoji}
        """.strip()
    
    def get_commands(self) -> Dict[str, str]:
        """
        Get a dictionary of available commands and their descriptions.
        
        Returns:
            Dict[str, str]: Command name -> description mapping
        """
        return {
            "hello": "Say hello to the bot",
            "info": "Get information about the bot",
            "help": "Show help message",
            "ping": "Test if the bot is responding",
            "status": "Get bot status information"
        }
    
    def is_development_mode(self) -> bool:
        """Check if the bot is running in development mode."""
        return self.development_mode
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration."""
        return {
            "url": self.database_url,
            "echo": self.development_mode,  # Show SQL queries in dev mode
        }

# Create a global instance that other modules can import
bot_config = BotConfig()
