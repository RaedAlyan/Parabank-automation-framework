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
    """Handles WebDriver initialization for supported browsers"""

    SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]

    def __init__(self):
        self.logger = Logger(__name__)
        self.config = ConfigLoader()
        self.browser = self.config.get_specified_browser()
        self._validate_browser()
        self.driver = None

    def _validate_browser(self):
        """Validate specified browser against the supported list"""
        if self.browser not in self.SUPPORTED_BROWSERS:
            self.logger.error(f'Unsupported browser: {self.browser}')
            raise ValueError(f'Unsupported browser: {self.browser}. Supported browsers are: {self.SUPPORTED_BROWSERS}')

    def initialize_webdriver(self):
        """
        Initializes and returns a WebDriver instance for the specified browser.

        :return: WebDriver instance.
        :raises WebDriverException: If an error occurs while initializing the webdriver.
        """
        try:
            self.logger.info(f'Initializing {self.browser.capitalize()} WebDriver...')
            options = self._get_browser_options()
            if self.browser == 'chrome':
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            elif self.browser == 'firefox':
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
            elif self.browser == 'edge':
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
            self.logger.info(f'{self.browser.capitalize()} WebDriver initialized successfully')
            return self.driver
        except WebDriverException as e:
            self.logger.error('WebDriver initialization failed!')
            raise WebDriverException('An error occurred while initializing the webdriver!') from e

    def _get_browser_options(self):
        """
        Returns the appropriate Options object populated with arguments based on browser settings.

        :return: Options object.
        """
        options = None
        if self.browser == 'chrome':
            options = webdriver.ChromeOptions()
        elif self.browser == 'firefox':
            options = webdriver.FirefoxOptions()
        elif self.browser == 'edge':
            options = webdriver.EdgeOptions()
        browser_options: list = self.config.get_browser_options(browser_name=self.browser).get('browser_options')
        self.logger.info(f'Applying this browser options "{browser_options}" to {self.browser.capitalize()} WebDriver')
        for option in browser_options:
            options.add_argument(option)
        return options
