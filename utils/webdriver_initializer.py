"""
WebDriver initializer module for the ParaBank automation framework

@author: Raed Eleyan
@date: 04/10/2025
@contact: raedeleyan1@gmail.com
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import WebDriverException
from .logger import Logger
from .config_loader import ConfigLoader


class WebDriverInitializer:
    """Handles WebDriver initialization"""

    SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]

    def __init__(self):
        self.logger = Logger(__name__)
        self.config = ConfigLoader()
        self.browser = self.config.get_specified_browser().lower()
        self._validate_browser()
        self.driver = None

    def _validate_browser(self):
        """Validate browser against supported list"""
        if self.browser not in self.SUPPORTED_BROWSERS:
            raise ValueError(f'Unsupported browser: {self.browser}. Use: {self.SUPPORTED_BROWSERS}')

    def initialize_webdriver(self):
        """
        Initializes and returns a WebDriver instance for the specified browser.

        :return: WebDriver instance.
        :raises WebDriverException: If an error occurs while initializing the webdriver.
        """
        try:
            self.logger.info(f'Initializing {self.browser.capitalize()} WebDriver...')
            if self.browser == 'chrome':
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif self.browser == 'firefox':
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            elif self.browser == 'edge':
                self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            self.logger.info(f'{self.browser.capitalize()} WebDriver initialized successfully')
            return self.driver
        except WebDriverException as e:
            self.logger.error('WebDriver initialization failed!')
            raise WebDriverException('An error occurred while initializing the webdriver!') from e
