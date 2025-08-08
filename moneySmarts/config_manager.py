import json
import os
import logging
from moneySmarts.exceptions import ConfigError

class ConfigManager:
    """
    Loads and manages application/game configuration from JSON files.
    Supports default settings and user-customizable overrides.

    Attributes:
        default_path (str): Path to the default configuration file.
        user_path (str): Path to the user configuration file.
        config (dict): Dictionary holding the merged configuration.
    """
    def __init__(self, default_path='config_default.json', user_path='config_user.json'):
        """
        Initialize ConfigManager with paths to default and user config files.

        Args:
            default_path (str): Path to the default configuration file.
            user_path (str): Path to the user configuration file.
        """
        self.default_path = default_path
        self.user_path = user_path
        self.config = {}
        self.load()

    def load(self):
        """Load configuration from default and user config files, with error handling and logging."""
        try:
            # Load default config
            if os.path.exists(self.default_path):
                with open(self.default_path, 'r') as f:
                    self.config = json.load(f)
            # Load user config and override defaults
            if os.path.exists(self.user_path):
                with open(self.user_path, 'r') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
        except (json.JSONDecodeError, OSError) as e:
            logging.error(f"Failed to load configuration: {e}")
            raise ConfigError(f"Failed to load configuration: {e}")

    def save_user_config(self):
        """Save current config as user settings to the user config file, with error handling and logging."""
        try:
            with open(self.user_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except OSError as e:
            logging.error(f"Failed to save user configuration: {e}")
            raise ConfigError(f"Failed to save user configuration: {e}")

    def get(self, key, default=None):
        """Get a configuration value by key, or return default if not found."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a configuration value and save to user config."""
        self.config[key] = value
        self.save_user_config()

# Singleton instance for global use
Config = ConfigManager()