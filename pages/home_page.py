"""
Home page class for the ParaBank automation framework

@author: Raed Eleyan
@date: 04/18/2025
@contact: raedeleyan1@gmail.com
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import Logger


class HomePage(BasePage):
    """Page Object Model for home page"""
    USERNAME_INPUT: tuple[str, str] = (By.CSS_SELECTOR, 'input[name="username"]')
    PASSWORD_INPUT: tuple[str, str] = (By.CSS_SELECTOR, 'input[name="password"]')
    LOGIN_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, 'input[class="button"]')
    USER_FULL_NAME: tuple[str, str] = (By.CSS_SELECTOR, 'p[class="smallText"]')
    MAIN_TITLE: tuple[str, str] = (By.XPATH, '//div[@id="showOverview"]//child::h1[@class="title"]')

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger(__name__)

    def login_user(self, username: str, password: str) -> None:
        """
        Logs in the user using the provided credentials.

        :param username: The username to log in with.
        :param password: The password to log in with.
        :raises Exception: When an error occurred while trying to log in with the provided credentials.
        """
        try:
            self.logger.info('Logging in...')
            self.send_keys(locator=self.USERNAME_INPUT, text=username)
            self.send_keys(locator=self.PASSWORD_INPUT, text=password)
            self.click(locator=self.LOGIN_BUTTON)
            self.logger.info('The user logged in successfully')
        except Exception as e:
            self.logger.error(f'Failed to log in. Error: {e}')
            raise Exception(f'An error occurred while trying to log in.') from e

    def get_user_full_name(self) -> str:
        """
         Retrieves the full name of the logged-in user.

        :return: The user's full name as displayed.
        :raises Exception: When an error occurred while trying to retrieve the user's full name.
        """
        try:
            self.logger.info('Retrieving the user full name...')
            web_element = self.find_element(locator=self.USER_FULL_NAME)
            self.logger.info(f'The user full name retrieved is: {web_element.text}')
            return web_element.text
        except Exception as e:
            self.logger.error(f'Failed to retrieve user full name. Error: {e}')
            raise Exception(f'An error occurred while retrieving the user full name.') from e

    def get_main_title(self) -> str:
        """
        Retrieves the main title text on the overview section of the home page.

        :return: The overview title string.
        :raises Exception: When an error occurred while trying to retrieve the overview title.
        """
        try:
            self.logger.info('Retrieving the main title...')
            web_element = self.find_element(locator=self.MAIN_TITLE)
            self.logger.info(f'The main title retrieved is: {web_element.text}')
            return web_element.text
        except Exception as e:
            self.logger.error(f'Failed to retrieve main title. Error: {e}')
            raise Exception(f'An error occurred while retrieving the main title.') from e
