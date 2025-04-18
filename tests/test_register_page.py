"""
Test module for the Register Page.

@author: Raed Eleyan
@date: 04/15/2025
@contact: raedeleyan1@gmail.com
"""
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.register_page import RegisterPage


@pytest.mark.order(1)
class TestRegisterPage:
    """Test suite for user registration functionality."""

    def test_register_new_user(self, browser: WebDriver, register_data: dict):
        """Test case to verify that a new user can register successfully."""
        browser.get('https://parabank.parasoft.com/parabank/register.htm')
        register_page = RegisterPage(browser)
        register_page.register_user(user_data=register_data)
        expected_welcome_message: str = f'Welcome {register_data["username"]}'
        actual_welcome_message: str = register_page.get_welcome_message()
        assert expected_welcome_message == actual_welcome_message, (
            f'The expected welcome message is {expected_welcome_message}, but the actual '
            f'welcome message is {actual_welcome_message}')

    @pytest.mark.parametrize("missing_field", ["first_name", "last_name", "address", "city", "state", "zip_code", "ssn",
                                               "username", "password", "confirm_password"])
    def test_register_with_missing_required_field_input(self, browser: WebDriver, register_data: dict,
                                                        missing_field: str):
        """Test case to verify registration fails when a required field is missing."""
        browser.get('https://parabank.parasoft.com/parabank/register.htm')
        user_data = register_data.copy()
        user_data.pop(missing_field)
        register_page = RegisterPage(browser)
        register_page.register_user(user_data=user_data)
        popup_error_message: str = register_page.get_popup_error_message(missing_field)
        assert popup_error_message is not None, (
            f'Expected an error message for missing field "{missing_field}", but none was found.'
        )
