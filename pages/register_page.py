"""
Register page class for the ParaBank automation framework

@author: Raed Eleyan
@date: 04/15/2025
@contact: raedeleyan1@gmail.com
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import Logger


class RegisterPage(BasePage):
    """Page Object Model for user registration page"""

    FIRST_NAME_INPUT = (By.ID, 'customer.firstName')
    LAST_NAME_INPUT = (By.ID, 'customer.lastName')
    ADDRESS_INPUT = (By.ID, 'customer.address.street')
    CITY_INPUT = (By.ID, 'customer.address.city')
    STATE_INPUT = (By.ID, 'customer.address.state')
    ZIP_CODE_INPUT = (By.ID, 'customer.address.zipCode')
    PHONE_INPUT = (By.ID, 'customer.phoneNumber')
    SSN_INPUT = (By.ID, 'customer.ssn')
    USERNAME_INPUT = (By.ID, 'customer.username')
    PASSWORD_INPUT = (By.ID, 'customer.password')
    CONFIRM_PASSWORD_INPUT = (By.ID, 'repeatedPassword')
    REGISTER_BUTTON = (By.CSS_SELECTOR, 'input[value="Register"]')
    POPUP_ERROR_MESSAGES = {
        'first_name': (By.ID, 'customer.firstName.errors'),
        'last_name': (By.ID, 'customer.lastName.errors'),
        'address': (By.ID, 'customer.address.street.errors'),
        'city': (By.ID, 'customer.address.city.errors'),
        'state': (By.ID, 'customer.address.state.errors'),
        'zip_code': (By.ID, 'customer.address.zipCode.errors'),
        'ssn': (By.ID, 'customer.ssn.errors'),
        'username': (By.ID, 'customer.username.errors'),
        'password': (By.ID, 'customer.password.errors'),
        'confirm_password': (By.ID, 'repeatedPassword.errors'),
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger(__name__)

    def register_user(self, user_data: dict) -> None:
        """
        Complete the registration form based on the provided data and submit it.

        :param user_data: A dict contains any subset of the following keys: first_name, last_name, address, city, state,
                          zip_code, phone, ssn, username, password, confirm_password.
        :raises Exception: When an error occurs while trying to register and submit the form.
        """
        locators_mapper = {
            'first_name': self.FIRST_NAME_INPUT,
            'last_name': self.LAST_NAME_INPUT,
            'address': self.ADDRESS_INPUT,
            'city': self.CITY_INPUT,
            'state': self.STATE_INPUT,
            'zip_code': self.ZIP_CODE_INPUT,
            'phone': self.PHONE_INPUT,
            'ssn': self.SSN_INPUT,
            'username': self.USERNAME_INPUT,
            'password': self.PASSWORD_INPUT,
            'confirm_password': self.CONFIRM_PASSWORD_INPUT,
        }
        try:
            self.fill_form_fields(user_data=user_data, locators_mapper=locators_mapper)
            self.click(locator=self.REGISTER_BUTTON)
        except Exception as e:
            self.logger.error(f'Failed to register the user! Error: {e}')
            raise Exception('An error occurred while trying to register the user!') from e

    def get_popup_error_message(self, missing_required_input_field: str) -> str:
        """
        Retrieves the popup error message for a missing required input field.

        :param missing_required_input_field: The name of the missing field.
        :return: The error message text displayed for the missing field.
        :raises ValueError: When the input field is unsupported.
        :raises Exception: When an error occurs while trying to retrieve the error message.
        """
        try:
            self.logger.info(f'The missing required input field is "{missing_required_input_field.capitalize()}"')
            locator = self.POPUP_ERROR_MESSAGES.get(missing_required_input_field.lower())
            if locator is None:
                raise ValueError(f'Unsupported input field: "{missing_required_input_field}"')
            welcome_element = self.find_element(locator)
            return welcome_element.text
        except Exception as e:
            self.logger.error(f'Failed to retrieve the popup error message! Error: {e}')
            raise Exception('An error occurred while retrieving the popup error message!') from e
