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

    FIRST_NAME_INPUT: tuple[str, str] = (By.ID, 'customer.firstName')
    LAST_NAME_INPUT: tuple[str, str] = (By.ID, 'customer.lastName')
    ADDRESS_INPUT: tuple[str, str] = (By.ID, 'customer.address.street')
    CITY_INPUT: tuple[str, str] = (By.ID, 'customer.address.city')
    STATE_INPUT: tuple[str, str] = (By.ID, 'customer.address.state')
    ZIP_CODE_INPUT: tuple[str, str] = (By.ID, 'customer.address.zipCode')
    PHONE_INPUT: tuple[str, str] = (By.ID, 'customer.phoneNumber')
    SSN_INPUT: tuple[str, str] = (By.ID, 'customer.ssn')
    USERNAME_INPUT: tuple[str, str] = (By.ID, 'customer.username')
    PASSWORD_INPUT: tuple[str, str] = (By.ID, 'customer.password')
    CONFIRM_PASSWORD_INPUT: tuple[str, str] = (By.ID, 'repeatedPassword')
    REGISTER_BUTTON: tuple[str, str] = (By.CSS_SELECTOR, 'input[value="Register"]')
    WELCOME_TITLE: tuple[str, str] = (By.CSS_SELECTOR, 'h1[class="title"]')
    POPUP_ERROR_MESSAGES: dict[str, tuple[str, str]] = {
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
        try:
            if 'first_name' in user_data:
                self.logger.info(f'Sending the first name "{user_data['first_name']}" to the registration form')
                self.send_keys(locator=self.FIRST_NAME_INPUT, text=user_data['first_name'])
            if 'last_name' in user_data:
                self.logger.info(f'Sending the last name "{user_data['last_name']}" to the registration form')
                self.send_keys(locator=self.LAST_NAME_INPUT, text=user_data['last_name'])
            if 'address' in user_data:
                self.logger.info(f'Sending the address "{user_data['address']}" to the registration form')
                self.send_keys(locator=self.ADDRESS_INPUT, text=user_data['address'])
            if 'city' in user_data:
                self.logger.info(f'Sending the city "{user_data['city']}" to the registration form')
                self.send_keys(locator=self.CITY_INPUT, text=user_data['city'])
            if 'state' in user_data:
                self.logger.info(f'Sending the state "{user_data['state']}" to the registration form')
                self.send_keys(locator=self.STATE_INPUT, text=user_data['state'])
            if 'zip_code' in user_data:
                self.logger.info(f'Sending the zip code "{user_data['zip_code']}" to the registration form')
                self.send_keys(locator=self.ZIP_CODE_INPUT, text=user_data['zip_code'])
            if 'phone' in user_data:
                self.logger.info(f'Sending the phone number "{user_data['phone']}" to the registration form')
                self.send_keys(locator=self.PHONE_INPUT, text=user_data['phone'])
            if 'ssn' in user_data:
                self.logger.info(f'Sending the ssn "{user_data['ssn']}" to the registration form')
                self.send_keys(locator=self.SSN_INPUT, text=user_data['ssn'])
            if 'username' in user_data:
                self.logger.info(f'Sending the username "{user_data['username']}" to the registration form')
                self.send_keys(locator=self.USERNAME_INPUT, text=user_data['username'])
            if 'password' in user_data:
                self.logger.info('Sending the password to the registration form')
                self.send_keys(locator=self.PASSWORD_INPUT, text=user_data['password'])
            if 'confirm_password' in user_data:
                self.logger.info('Sending the confirmation password to the registration form')
                self.send_keys(locator=self.CONFIRM_PASSWORD_INPUT, text=user_data['confirm_password'])
            self.click(locator=self.REGISTER_BUTTON)
        except Exception as e:
            self.logger.error(f'Failed to register the user! Error: {e}')
            raise Exception('An error occurred while trying to register the user!') from e

    def get_welcome_message(self) -> str:
        """
        Retrieves the displayed welcome message that is presented after the user is registered successfully.

        :return: The welcome message.
        """
        welcome_element = self.find_element(locator=self.WELCOME_TITLE)
        return welcome_element.text

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
