#!/usr/bin/env python3
"""
Generate BSCI Slackbot - Main Entry Point
==========================================

This is the main file that starts the Slack bot.
Run this file to start the bot: python main.py

For new team members:
- This file sets up the bot and connects it to Slack
- It imports all the handlers and commands
- It starts the bot server and keeps it running
"""

import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Import our custom handlers and commands
from handlers.message_handler import setup_message_handlers
from handlers.command_handler import setup_command_handlers
from handlers.event_handler import setup_event_handlers
from config.settings import BotConfig

# Load environment variables from .env file
load_dotenv()

# Set up logging so we can see what the bot is doing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_bot_app():
    """
    Create and configure the Slack bot app.
    
    This function:
    1. Creates a new Slack app instance
    2. Sets up all the handlers (message, command, event)
    3. Returns the configured app
    """
    logger.info("🤖 Creating Slack bot app...")
    
    # Create the Slack app with our bot token
    app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SIGNING_SECRET")
    )
    
    # Set up all our handlers
    logger.info("📝 Setting up message handlers...")
    setup_message_handlers(app)
    
    logger.info("⚡ Setting up command handlers...")
    setup_command_handlers(app)
    
    logger.info("🎯 Setting up event handlers...")
    setup_event_handlers(app)
    
    logger.info("✅ Bot app created successfully!")
    return app

def main():
    """
    Main function that starts the bot.
    
    This function:
    1. Checks that all required environment variables are set
    2. Creates the bot app
    3. Starts the bot using Socket Mode (real-time communication)
    """
    logger.info("🚀 Starting Generate BSCI Slackbot...")
    
    # Check that we have all the required environment variables
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "SIGNING_SECRET"]
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file and make sure all required variables are set.")
        return
    
    # Create the bot app
    app = create_bot_app()
    
    # Get the app-level token for Socket Mode
    app_token = os.environ.get("SLACK_APP_TOKEN")
    
    # Start the bot using Socket Mode
    # Socket Mode allows real-time communication with Slack
    logger.info("🔌 Connecting to Slack using Socket Mode...")
    logger.info("💡 The bot is now running! Press Ctrl+C to stop.")
    
    try:
        handler = SocketModeHandler(app, app_token)
        handler.start()
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user.")
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        logger.error("Please check your tokens and try again.")

if __name__ == "__main__":
    # This runs when you execute: python main.py
    main()
