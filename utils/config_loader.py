"""
Configuration loader utility for the ParaBank automation framework.

Handles reading and parsing JSON configuration files for browser settings,
environment parameters, and framework configurations.

@author: Raed Eleyan
@date: 04/07/2025
@contact: raedeleyan1@gmail.com
"""
import json
import logging
from pathlib import Path


class ConfigLoader:
    """Utility class for loading and managing framework configuration files."""

    def __init__(self, config_path: str = '../config/config.json'):
        self.logger = logging.Logger(__name__)
        self.config_path = Path(config_path).resolve()
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """
        Retrieves the contents of the config.json file.

        :return: the contents of the configuration file.
        :raises FileNotFoundError: if the configuration file doesn't exist.
        :raises json.JSONDecodeError: if the configuration file contains invalid JSON format.
        """
        try:
            self.logger.info(f'Loading configuration from {self.config_path}')
            with open(self.config_path) as f:
                config = json.load(f)
            self.logger.info(f'Loaded configuration from {self.config_path} successfully')
            return config
        except FileNotFoundError as e:
            self.logger.error(f'Configuration file not found at {self.config_path}')
            raise e
        except json.JSONDecodeError as e:
            self.logger.error(f'Invalid JSON format in the configuration file')
            raise e

    def get_specified_browser(self) -> str:
        """
        Retrieves the specified browser from the configuration file.

        :return: The specified browser name.
        :raises ValueError: If no browser is specified.
        :raises KeyError: If 'browser' key is missing in configuration file.
        """
        try:
            specified_browser = self.config.get('browser')
            if specified_browser is None:
                raise ValueError('No browser specified in the configuration file')
            self.logger.info(f'The specified browser is: {specified_browser}')
            return specified_browser
        except KeyError:
            self.logger.error("Missing 'browser' key in the configuration file")
            raise KeyError("Required 'browser' key missing in the configuration file")
