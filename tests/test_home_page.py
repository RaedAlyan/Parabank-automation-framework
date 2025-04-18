"""
Test module for the Home Page.

@author: Raed Eleyan
@date: 04/18/2025
@contact: raedeleyan1@gmail.com
"""
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.home_page import HomePage


@pytest.mark.order(2)
class TestHomePage:

    def test_login_functionality(self, browser: WebDriver, register_data: dict):
        """Test case to verify that the registered user can log in successfully"""
        browser.get('https://parabank.parasoft.com/parabank/index.htm')
        home_page = HomePage(browser)
        home_page.login_user(username=register_data['username'], password=register_data['password'])
        expected_full_name = f'Welcome {register_data["first_name"]} {register_data["last_name"]}'
        expected_main_title = 'Accounts Overview'
        actual_full_name = home_page.get_user_full_name()
        actual_main_title = home_page.get_main_title()
        assert expected_full_name == actual_full_name, (
            f'The full name of the account is incorrect. The expected full name is {expected_full_name}, but the '
            f'actual full name is {actual_full_name}.'
        )
        assert expected_main_title == actual_main_title, (
            f'The main title of the account is incorrect. The expected main title is {expected_main_title}, but the '
            f'actual main title is {actual_main_title}.'
        )
