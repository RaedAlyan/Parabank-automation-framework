"""

@author: Raed Eleyan
@date: 04/15/2025
@contact: raedeleyan1@gmail.com
"""
from selenium.webdriver.common.by import By
from base_page import BasePage
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

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = Logger(__name__)

    def register_user(self, first_name: str, last_name: str, address: str, city: str, state: str, zip_code: str,
                      phone: str, ssn: str, username: str, password: str, confirm_password: str) -> None:
        """
        Complete registration form and submit

        :param first_name: User's first name.
        :param last_name: User's last name.
        :param address: User's street address.
        :param city: User's city.
        :param state: State/province.
        :param zip_code: Zip/postal code.
        :param phone: Phone number.
        :param ssn: Social Security Number.
        :param username: Desired username.
        :param password: Account password.
        :param confirm_password: Password confirmation.
        """
        self.logger.info(
            f"Start registering the user with this information:\n"
            f"First Name: {first_name}, Last Name: {last_name}\n"
            f"Address: {address}, City: {city}, State: {state}, Zip Code: {zip_code}\n"
            f"Phone: {phone}, SSN: {ssn}, Username: {username}"
        )
        try:
            self.send_keys(locator=self.FIRST_NAME_INPUT, text=first_name)
            self.send_keys(locator=self.LAST_NAME_INPUT, text=last_name)
            self.send_keys(locator=self.ADDRESS_INPUT, text=address)
            self.send_keys(locator=self.CITY_INPUT, text=city)
            self.send_keys(locator=self.STATE_INPUT, text=state)
            self.send_keys(locator=self.ZIP_CODE_INPUT, text=zip_code)
            self.send_keys(locator=self.PHONE_INPUT, text=phone)
            self.send_keys(locator=self.SSN_INPUT, text=ssn)
            self.send_keys(locator=self.USERNAME_INPUT, text=username)
            self.send_keys(locator=self.PASSWORD_INPUT, text=password)
            self.send_keys(locator=self.CONFIRM_PASSWORD_INPUT, text=confirm_password)
            self.click(locator=self.REGISTER_BUTTON)
        except Exception as e:
            self.logger.error(f'Failed to register the user! Error: {e}')
            raise Exception('An error occurred while trying to register the user!') from e
