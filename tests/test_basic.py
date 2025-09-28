"""
Basic Tests
===========

This file contains basic tests for the Slackbot.
These tests help ensure the bot is working correctly.

For new team members:
- Run tests with: python -m pytest tests/
- Add new tests here when you add new features
- Tests help catch bugs before they reach users
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import (
    format_user_mention,
    extract_user_id_from_mention,
    truncate_message,
    parse_command_args,
    is_valid_email,
    sanitize_text,
    validate_slack_token
)

class TestHelpers:
    """Test helper functions."""
    
    def test_format_user_mention(self):
        """Test formatting user mentions."""
        user_id = "U1234567890"
        mention = format_user_mention(user_id)
        assert mention == "<@U1234567890>"
    
    def test_extract_user_id_from_mention(self):
        """Test extracting user ID from mentions."""
        mention = "<@U1234567890>"
        user_id = extract_user_id_from_mention(mention)
        assert user_id == "U1234567890"
        
        # Test invalid mention
        invalid_mention = "not a mention"
        user_id = extract_user_id_from_mention(invalid_mention)
        assert user_id is None
    
    def test_truncate_message(self):
        """Test message truncation."""
        long_message = "a" * 5000
        truncated = truncate_message(long_message, 100)
        assert len(truncated) <= 100
        assert truncated.endswith("...")
        
        # Test short message (should not be truncated)
        short_message = "Hello world"
        result = truncate_message(short_message)
        assert result == short_message
    
    def test_parse_command_args(self):
        """Test parsing command arguments."""
        text = "hello world test"
        args = parse_command_args(text)
        assert args == ["hello", "world", "test"]
        
        # Test with extra spaces
        text = "  hello   world  test  "
        args = parse_command_args(text)
        assert args == ["hello", "world", "test"]
        
        # Test empty string
        args = parse_command_args("")
        assert args == []
    
    def test_is_valid_email(self):
        """Test email validation."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "test+tag@example.org"
        ]
        
        invalid_emails = [
            "notanemail",
            "@example.com",
            "test@",
            "test@.com"
        ]
        
        for email in valid_emails:
            assert is_valid_email(email) is True
        
        for email in invalid_emails:
            assert is_valid_email(email) is False
    
    def test_sanitize_text(self):
        """Test text sanitization."""
        text = "<script>alert('hello')</script>"
        sanitized = sanitize_text(text)
        assert "<" not in sanitized
        assert ">" not in sanitized
        
        # Test normal text (should not change)
        normal_text = "Hello world"
        result = sanitize_text(normal_text)
        assert result == normal_text
    
    def test_validate_slack_token(self):
        """Test Slack token validation."""
        valid_tokens = [
            "xoxb-1234567890-1234567890123-abcdefghijklmnopqrstuvwx",
            "xoxp-1234567890-1234567890123-abcdefghijklmnopqrstuvwx",
            "xoxa-1234567890-1234567890123-abcdefghijklmnopqrstuvwx"
        ]
        
        invalid_tokens = [
            "invalid-token",
            "xox-1234567890",
            "",
            None
        ]
        
        for token in valid_tokens:
            assert validate_slack_token(token) is True
        
        for token in invalid_tokens:
            assert validate_slack_token(token) is False

class TestConfig:
    """Test configuration settings."""
    
    def test_bot_config_import(self):
        """Test that we can import the bot config."""
        try:
            from config.settings import bot_config
            assert bot_config is not None
            assert hasattr(bot_config, 'bot_name')
            assert hasattr(bot_config, 'get_commands')
        except ImportError:
            pytest.skip("Bot config not available")

class TestCommands:
    """Test command functions."""
    
    def test_help_command_import(self):
        """Test that we can import help command functions."""
        try:
            from commands.help import get_help_response, get_quick_help
            assert callable(get_help_response)
            assert callable(get_quick_help)
        except ImportError:
            pytest.skip("Help commands not available")
    
    def test_info_command_import(self):
        """Test that we can import info command functions."""
        try:
            from commands.info import get_bot_info, get_system_status
            assert callable(get_bot_info)
            assert callable(get_system_status)
        except ImportError:
            pytest.skip("Info commands not available")
    
    def test_greeting_command_import(self):
        """Test that we can import greeting command functions."""
        try:
            from commands.greeting import handle_greeting_command, get_greeting_message
            assert callable(handle_greeting_command)
            assert callable(get_greeting_message)
        except ImportError:
            pytest.skip("Greeting commands not available")

# Run tests if this file is executed directly
if __name__ == "__main__":
    pytest.main([__file__])
