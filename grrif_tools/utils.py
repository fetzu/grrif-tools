"""
Common utilities for GRRIF Tools.

This module provides utilities for file paths, configuration, and logging.
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union
import configparser

# Set up logging
logger = logging.getLogger("grrif_tools")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Create user data directory
def get_user_data_dir() -> Path:
    """Get the user data directory for storing GRRIF Tools data."""
    data_dir = Path.home() / "grrif_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

# Get database path
def get_database_path() -> Path:
    """Get the path to the SQLite database."""
    return get_user_data_dir() / "grrif_data.db"

# Get plays directory path
def get_plays_dir() -> Path:
    """Get the directory for storing play history text files."""
    plays_dir = get_user_data_dir() / "plays"
    plays_dir.mkdir(exist_ok=True)
    return plays_dir

# Get config path
def get_config_path() -> Path:
    """Get the path to the configuration file."""
    return get_user_data_dir() / "config.ini"

# Get buffer file path
def get_buffer_path() -> Path:
    """Get the path to the audio buffer file."""
    return get_user_data_dir() / "buferr.mp3"

# Config management class
class Config:
    """Configuration manager for GRRIF Tools."""
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from file."""
        self._config = configparser.ConfigParser()
        config_path = get_config_path()
        
        if config_path.exists():
            self._config.read(config_path)
        
        # Ensure default sections exist
        if 'lastfm' not in self._config:
            self._config['lastfm'] = {}
        if 'general' not in self._config:
            self._config['general'] = {'default_start_date': '2021-01-01'}
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(section, key, fallback=fallback)
    
    def set(self, section: str, key: str, value: str) -> None:
        """Set a configuration value."""
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        self._save_config()
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        with open(get_config_path(), 'w') as configfile:
            self._config.write(configfile)
            
    def get_lastfm_credentials(self) -> Dict[str, str]:
        """Get Last.fm API credentials."""
        return {
            'api_key': self.get('lastfm', 'api_key', ''),
            'api_secret': self.get('lastfm', 'api_secret', ''),
            'session_key': self.get('lastfm', 'session_key', '')
        }
    
    def set_lastfm_credentials(self, api_key: str, api_secret: str, session_key: str) -> None:
        """Set Last.fm API credentials."""
        self.set('lastfm', 'api_key', api_key)
        self.set('lastfm', 'api_secret', api_secret)
        self.set('lastfm', 'session_key', session_key)
