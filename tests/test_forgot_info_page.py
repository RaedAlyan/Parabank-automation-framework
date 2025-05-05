"""
Test module for the Forgot Info Page.

@author: Raed Eleyan
@date: 05/05/2025
@contact: raedeleyan1@gmail.com
"""
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.forgot_info_page import ForgotInfoPage


@pytest.mark.order(3)
class TestForgotInfoPage:
    """Test suite for the 'Forgot Login Info' page functionality."""


    def test_perform_forgot_info(self, browser: WebDriver, register_data: dict):
        """Test case to verify that the user can retrieve their username and password using the Forgot Info page"""
        browser.get('https://parabank.parasoft.com/parabank/lookup.htm')
        forgot_info_form_fields = ['first_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'ssn']
        forgot_info_data = {key: register_data[key] for key in forgot_info_form_fields}
        forgot_info_page = ForgotInfoPage(browser)
        forgot_info_page.perform_lookup_customer(user_data=forgot_info_data)
        expected_welcome_message = 'Customer Lookup'
        actual_welcome_message: str = forgot_info_page.get_welcome_message()
        expected_paragraph = 'Your login information was located successfully. You are now logged in.'
        actual_paragraph = forgot_info_page.get_displayed_paragraph()
        credentials = forgot_info_page.get_credentials()
        expected_username = register_data['username']
        actual_username = credentials['username']
        expected_password = register_data['password']
        actual_password = credentials['password']
        assert expected_welcome_message == actual_welcome_message, (
            f'The expected welcome message is {expected_welcome_message}, but the actual '
            f'welcome message is {actual_welcome_message}')
        assert expected_paragraph == actual_paragraph, (
            f'The expected paragraph is {expected_paragraph}, but the actual '
            f'paragraph is {actual_paragraph}'
        )
        assert expected_username == actual_username, (
            f'The expected username is {expected_username}, but the actual '
            f'username is {actual_username}'
        )
        assert expected_password == actual_password, (
            f'The expected password is {expected_password}, but the actual '
            f'password is {actual_password}'
        )
