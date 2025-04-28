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

    def __init__(self, config_path: str = 'config/config.json'):
        self.logger = logging.getLogger(__name__)
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
            with open(self.config_path) as file:
                config = json.load(file)
            self.logger.info('Configurations loaded successfully')
            return config
        except FileNotFoundError as e:
            self.logger.error(f'Configuration file not found at {self.config_path}')
            raise FileNotFoundError(f'Configuration file could not be found. Error: {e}') from e
        except json.JSONDecodeError as e:
            self.logger.error(f'Invalid JSON format in the configuration file')
            raise json.JSONDecodeError(f'Invalid JSON format: {e.msg}', e.doc, e.pos)

    def get_specified_browser(self) -> str:
        """
        Retrieves the specified browser from the configuration file.

        :return: The specified browser name.
        :raises ValueError: If no browser is specified.
        """
        specified_browser = self.config.get('browser')
        if specified_browser is None:
            raise ValueError('No browser specified in the configuration file')
        self.logger.info(f'The specified browser is: {specified_browser}')
        return specified_browser.lower()

    def get_browser_options(self, browser_name: str) -> dict:
        """
        Retrieves the specified browser options

        :param browser_name: The name of the specified browser.
        :return: The specified browser options.
        :raises ValueError: If no configuration is found for the specified browser.
        """
        self.logger.info('Retrieving the browser options from configuration file')
        browser_options = self.config.get(browser_name)
        if browser_options is None:
            self.logger.error('Browser options aren\'t found in the configuration file for this browser: '
                              f'{browser_name}')
            raise ValueError(f'No specified options found for this browser: {browser_name}')
        self.logger.info(f'The specified options for this browser "{browser_name}" are: {browser_options}')
        return browser_options
