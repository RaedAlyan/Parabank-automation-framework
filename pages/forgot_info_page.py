"""
Forgot info page class for the ParaBank automation framework

@author: Raed Eleyan
@date: 05/05/2025
@contact: raedeleyan1@gmail.com
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import Logger


class ForgotInfoPage(BasePage):
    """Page object model for the 'Forgot Login Info' page."""

    FIRST_NAME_INPUT = (By.ID, 'firstName')
    LAST_NAME_INPUT = (By.ID, 'lastName')
    ADDRESS_INPUT = (By.ID, 'address.street')
    CITY_INPUT = (By.ID, 'address.city')
    STATE_INPUT = (By.ID, 'address.state')
    ZIP_CODE_INPUT = (By.ID, 'address.zipCode')
    SSN_INPUT = (By.ID, 'ssn')
    FIND_MY_LOGIN_INFO_BUTTON = (By.XPATH, '//input[@type="submit" and @value="Find My Login Info"]')
    CURRENT_PARAGRAPH = (By.XPATH, '//div[@id="rightPanel"]/descendant::p[1]')
    CREDENTIALS_PARAGRAPH = (By.XPATH, '//div[@id="rightPanel"]//descendant::p[2]')

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger(__name__)

    def perform_lookup_customer(self, user_data: dict) -> None:
        """
        Performs a customer lookup using the provided user data.

        :param user_data: A dictionary containing the customer information.
        :raises Exception: when an error occurs while trying to perform the customer lookup.
        """
        locators_mapper = {
            'first_name': self.FIRST_NAME_INPUT,
            'last_name': self.LAST_NAME_INPUT,
            'address': self.ADDRESS_INPUT,
            'city': self.CITY_INPUT,
            'state': self.STATE_INPUT,
            'zip_code': self.ZIP_CODE_INPUT,
            'ssn': self.SSN_INPUT,
        }
        try:
            self.logger.info(f'Attempting to look up customer with data: {user_data}')
            self.fill_form_fields(user_data=user_data, locators_mapper=locators_mapper)
            self.click(locator=self.FIND_MY_LOGIN_INFO_BUTTON)
            self.logger.info('Customer lookup submitted successfully.')
        except Exception as e:
            self.logger.error(f'Customer lookup failed! Error: {e}')
            raise Exception('An error occurred while trying to perform customer lookup.')

    def get_displayed_paragraph(self) -> str:
        """
        Retrieves the paragraph displayed after a successful customer lookup.

        :return: Text content of the confirmation paragraph.
        """
        return self.find_element(locator=self.CURRENT_PARAGRAPH).text

    def get_credentials(self) -> dict:
        """
        Extracts and returns the username and password from the credentials paragraph.

        :return: A dictionary with keys 'username' and 'password'.
        """
        try:
            credentials = {}
            text = self.find_element(locator=self.CREDENTIALS_PARAGRAPH).text
            lines = text.splitlines()
            for line in lines:
                key, value = line.split(':')
                credentials[key.strip().lower()] = value.strip()
            self.logger.info(f'Credentials extracted successfully.')
            return credentials
        except Exception as e:
            self.logger.error(f'Credentials extraction failed! Error: {e}')
            raise Exception('An error occurred while trying to extract credentials.')
