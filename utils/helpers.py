"""
Helper Functions
================

This file contains utility functions that can be used throughout the bot.
These are common functions that multiple parts of the bot might need.

For new team members:
- Add new utility functions here
- Keep functions simple and focused on one task
- Add clear documentation for each function
- Test your functions before using them
"""

import logging
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def format_user_mention(user_id: str) -> str:
    """
    Format a user ID as a Slack mention.
    
    Args:
        user_id: The Slack user ID
        
    Returns:
        str: Formatted user mention (e.g., "<@U1234567890>")
    """
    return f"<@{user_id}>"

def extract_user_id_from_mention(mention: str) -> Optional[str]:
    """
    Extract user ID from a Slack mention.
    
    Args:
        mention: The mention string (e.g., "<@U1234567890>")
        
    Returns:
        Optional[str]: The user ID or None if not a valid mention
    """
    match = re.match(r'<@([UW][A-Z0-9]+)>', mention)
    return match.group(1) if match else None

def format_channel_mention(channel_id: str) -> str:
    """
    Format a channel ID as a Slack channel mention.
    
    Args:
        channel_id: The Slack channel ID
        
    Returns:
        str: Formatted channel mention (e.g., "<#C1234567890>")
    """
    return f"<#{channel_id}>"

def format_timestamp(timestamp: float) -> str:
    """
    Format a Unix timestamp as a readable date string.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        str: Formatted date string
    """
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return "Invalid timestamp"

def truncate_message(message: str, max_length: int = 4000) -> str:
    """
    Truncate a message to fit within Slack's message limits.
    
    Args:
        message: The message to truncate
        max_length: Maximum length (default: 4000 for Slack)
        
    Returns:
        str: Truncated message
    """
    if len(message) <= max_length:
        return message
    
    # Truncate and add ellipsis
    truncated = message[:max_length - 3] + "..."
    logger.warning(f"Message truncated from {len(message)} to {len(truncated)} characters")
    return truncated

def parse_command_args(text: str) -> List[str]:
    """
    Parse command arguments from a message.
    
    Args:
        text: The message text
        
    Returns:
        List[str]: List of arguments
    """
    # Split by whitespace and remove empty strings
    args = [arg.strip() for arg in text.split() if arg.strip()]
    return args

def is_valid_email(email: str) -> bool:
    """
    Check if a string is a valid email address.
    
    Args:
        email: The email string to validate
        
    Returns:
        bool: True if valid email, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing potentially harmful characters.
    
    Args:
        text: The text to sanitize
        
    Returns:
        str: Sanitized text
    """
    # Remove or escape potentially problematic characters
    # This is a basic sanitization - adjust based on your needs
    sanitized = text.replace('<', '&lt;').replace('>', '&gt;')
    return sanitized

def create_slack_block(text: str, block_type: str = "section") -> Dict[str, Any]:
    """
    Create a Slack block element.
    
    Args:
        text: The text content
        block_type: The type of block (section, header, divider, etc.)
        
    Returns:
        Dict[str, Any]: Slack block dictionary
    """
    if block_type == "section":
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
    elif block_type == "header":
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": text
            }
        }
    elif block_type == "divider":
        return {
            "type": "divider"
        }
    else:
        # Default to section
        return create_slack_block(text, "section")

def create_button(text: str, action_id: str, value: str = "", style: str = "primary") -> Dict[str, Any]:
    """
    Create a Slack button element.
    
    Args:
        text: The button text
        action_id: The action ID for the button
        value: The value to send when clicked
        style: The button style (primary, danger, or default)
        
    Returns:
        Dict[str, Any]: Slack button dictionary
    """
    button = {
        "type": "button",
        "text": {
            "type": "plain_text",
            "text": text
        },
        "action_id": action_id,
        "value": value or text.lower().replace(" ", "_")
    }
    
    if style in ["primary", "danger"]:
        button["style"] = style
    
    return button

def create_help_blocks(commands: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Create help blocks for displaying available commands.
    
    Args:
        commands: Dictionary of command names and descriptions
        
    Returns:
        List[Dict[str, Any]]: List of Slack blocks
    """
    blocks = []
    
    # Header
    blocks.append(create_slack_block("🤖 *Available Commands*", "header"))
    blocks.append(create_slack_block("", "divider"))
    
    # Commands
    for command, description in commands.items():
        blocks.append(create_slack_block(f"• `/{command}` - {description}"))
    
    # Footer
    blocks.append(create_slack_block("", "divider"))
    blocks.append(create_slack_block("Need more help? Ask the development team! 💬"))
    
    return blocks

def log_user_action(user_id: str, action: str, details: str = ""):
    """
    Log a user action for debugging and monitoring.
    
    Args:
        user_id: The user who performed the action
        action: The action performed
        details: Additional details about the action
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] User {user_id}: {action}"
    
    if details:
        log_message += f" - {details}"
    
    logger.info(log_message)

def validate_slack_token(token: str) -> bool:
    """
    Validate a Slack token format.
    
    Args:
        token: The token to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not token:
        return False
    
    # Check for valid Slack token prefixes
    valid_prefixes = ["xoxb-", "xoxp-", "xoxa-", "xoxr-", "xoxs-", "xoxo-"]
    return any(token.startswith(prefix) for prefix in valid_prefixes)

def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary with a default.
    
    Args:
        dictionary: The dictionary to get the value from
        key: The key to look for
        default: The default value if key is not found
        
    Returns:
        Any: The value or default
    """
    try:
        return dictionary.get(key, default)
    except (AttributeError, TypeError):
        return default
