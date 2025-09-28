"""
Info Command
============

This command provides information about the bot.
It shows version, status, and other useful details.

For new team members:
- This command is already registered in the command handler
- You can modify the bot information here
- Update version numbers when you make changes
"""

import logging
import platform
import sys
from datetime import datetime
from config.settings import bot_config

logger = logging.getLogger(__name__)

def get_bot_info() -> dict:
    """
    Get comprehensive bot information.
    
    Returns:
        dict: Bot information data
    """
    logger.info("Generating bot info response")
    
    # Get system information
    python_version = sys.version.split()[0]
    platform_info = platform.system()
    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the info response
    info_text = f"""
*{bot_config.bot_name} Information*

🤖 **Bot Details:**
• Name: {bot_config.bot_name}
• Version: 1.0.0
• Status: 🟢 Online and Healthy
• Development Mode: {'Yes' if bot_config.is_development_mode() else 'No'}

⚙️ **System Information:**
• Python Version: {python_version}
• Platform: {platform_info}
• Current Time: {current_time}

📊 **Statistics:**
• Commands Available: {len(bot_config.get_commands())}
• Default Channel: {bot_config.default_channel}
• Max Message Length: {bot_config.max_message_length} characters

🛠️ **Technical Details:**
• Framework: Slack Bolt for Python
• Database: SQLite (optional)
• Logging: Python logging module
• Environment: {'Development' if bot_config.is_development_mode() else 'Production'}

💡 **Need Help?**
Type `/help` for available commands or mention me in a channel!
    """.strip()
    
    response = {
        "response_type": "ephemeral",
        "text": "🤖 Bot Information",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": info_text
                }
            }
        ]
    }
    
    return response

def get_system_status() -> dict:
    """
    Get system status information.
    
    Returns:
        dict: System status data
    """
    try:
        # Get basic system info
        import psutil
        
        # CPU and memory info
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        status_text = f"""
*System Status Report*

🖥️ **System Resources:**
• CPU Usage: {cpu_percent}%
• Memory Usage: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
• Available Memory: {memory.available // (1024**3)}GB

📊 **Bot Health:**
• Status: 🟢 Healthy
• Uptime: All systems operational
• Last Check: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """.strip()
        
    except ImportError:
        # psutil not available, show basic info
        status_text = f"""
*System Status Report*

📊 **Bot Health:**
• Status: 🟢 Healthy
• Uptime: All systems operational
• Last Check: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
• Note: Detailed system info not available (psutil not installed)
        """.strip()
    
    return {
        "response_type": "ephemeral",
        "text": "📊 System Status",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": status_text
                }
            }
        ]
    }

def get_development_info() -> dict:
    """
    Get development information (only shown in development mode).
    
    Returns:
        dict: Development info data
    """
    if not bot_config.is_development_mode():
        return {
            "response_type": "ephemeral",
            "text": "Development information is only available in development mode."
        }
    
    dev_info = f"""
*Development Information*

🔧 **Development Mode Active**

📁 **Project Structure:**
• Main Bot File: `main.py`
• Handlers: `handlers/` directory
• Commands: `commands/` directory
• Utilities: `utils/` directory
• Configuration: `config/settings.py`

🐛 **Debug Information:**
• Log Level: {bot_config.log_level}
• Database: {bot_config.database_url}
• Default Channel: {bot_config.default_channel}

📝 **For Developers:**
• Add new commands in `commands/` directory
• Modify handlers in `handlers/` directory
• Update configuration in `config/settings.py`
• Check logs for debugging information

⚠️ **Note:** This information is only visible in development mode.
    """.strip()
    
    return {
        "response_type": "ephemeral",
        "text": "🔧 Development Info",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": dev_info
                }
            }
        ]
    }
