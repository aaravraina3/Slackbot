"""
Database Utilities
==================

This file contains database-related functions for the bot.
You can use this to store and retrieve data if needed.

For new team members:
- This is optional - you don't need a database for basic bot functionality
- Use this if you want to store user preferences, command history, etc.
- SQLite is used by default (simple file-based database)
"""

import sqlite3
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BotDatabase:
    """
    Simple database class for the Slackbot.
    
    This class handles database operations using SQLite.
    It's designed to be simple and easy to use for beginners.
    """
    
    def __init__(self, db_path: str = "bot_database.db"):
        """
        Initialize the database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """
        Initialize the database and create tables if they don't exist.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create users table to store user information
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        username TEXT,
                        real_name TEXT,
                        email TEXT,
                        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        command_count INTEGER DEFAULT 0
                    )
                """)
                
                # Create commands table to store command history
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS commands (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        command TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        channel_id TEXT,
                        success BOOLEAN DEFAULT TRUE,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                """)
                
                # Create settings table for bot configuration
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def add_user(self, user_id: str, username: str, real_name: str = "", email: str = ""):
        """
        Add a new user to the database.
        
        Args:
            user_id: Slack user ID
            username: Slack username
            real_name: User's real name
            email: User's email (optional)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO users (user_id, username, real_name, email, last_seen)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (user_id, username, real_name, email))
                conn.commit()
                logger.info(f"User {username} added/updated in database")
        except Exception as e:
            logger.error(f"Error adding user: {e}")
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from the database.
        
        Args:
            user_id: Slack user ID
            
        Returns:
            Optional[Dict[str, Any]]: User information or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def update_user_last_seen(self, user_id: str):
        """
        Update the last seen timestamp for a user.
        
        Args:
            user_id: Slack user ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET last_seen = CURRENT_TIMESTAMP 
                    WHERE user_id = ?
                """, (user_id,))
                conn.commit()
        except Exception as e:
            logger.error(f"Error updating user last seen: {e}")
    
    def increment_command_count(self, user_id: str):
        """
        Increment the command count for a user.
        
        Args:
            user_id: Slack user ID
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET command_count = command_count + 1 
                    WHERE user_id = ?
                """, (user_id,))
                conn.commit()
        except Exception as e:
            logger.error(f"Error incrementing command count: {e}")
    
    def log_command(self, user_id: str, command: str, channel_id: str, success: bool = True):
        """
        Log a command execution.
        
        Args:
            user_id: Slack user ID
            command: The command that was executed
            channel_id: The channel where the command was executed
            success: Whether the command was successful
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO commands (user_id, command, channel_id, success)
                    VALUES (?, ?, ?, ?)
                """, (user_id, command, channel_id, success))
                conn.commit()
                logger.info(f"Command logged: {command} by {user_id}")
        except Exception as e:
            logger.error(f"Error logging command: {e}")
    
    def get_command_stats(self) -> Dict[str, Any]:
        """
        Get command usage statistics.
        
        Returns:
            Dict[str, Any]: Command statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total commands
                cursor.execute("SELECT COUNT(*) FROM commands")
                total_commands = cursor.fetchone()[0]
                
                # Most used commands
                cursor.execute("""
                    SELECT command, COUNT(*) as count 
                    FROM commands 
                    GROUP BY command 
                    ORDER BY count DESC 
                    LIMIT 5
                """)
                top_commands = cursor.fetchall()
                
                # Most active users
                cursor.execute("""
                    SELECT user_id, COUNT(*) as count 
                    FROM commands 
                    GROUP BY user_id 
                    ORDER BY count DESC 
                    LIMIT 5
                """)
                top_users = cursor.fetchall()
                
                return {
                    "total_commands": total_commands,
                    "top_commands": top_commands,
                    "top_users": top_users
                }
        except Exception as e:
            logger.error(f"Error getting command stats: {e}")
            return {"total_commands": 0, "top_commands": [], "top_users": []}
    
    def set_setting(self, key: str, value: str):
        """
        Set a bot setting.
        
        Args:
            key: Setting key
            value: Setting value
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO settings (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (key, value))
                conn.commit()
                logger.info(f"Setting {key} updated")
        except Exception as e:
            logger.error(f"Error setting setting: {e}")
    
    def get_setting(self, key: str, default: str = "") -> str:
        """
        Get a bot setting.
        
        Args:
            key: Setting key
            default: Default value if setting not found
            
        Returns:
            str: Setting value or default
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                return row[0] if row else default
        except Exception as e:
            logger.error(f"Error getting setting: {e}")
            return default
    
    def close(self):
        """
        Close the database connection.
        Note: This is handled automatically by the context manager.
        """
        pass

# Create a global database instance
# This will be initialized when the module is imported
db = BotDatabase()
