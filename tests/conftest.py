"""
Pytest configuration and fixtures for ParaBank automation framework

@author: Raed Eleyan
@date: 04/10/2025
@contact: raedeleyan1@gmail.com
"""
import sys
import os
import pytest
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from utils.logger import Logger
from utils.webdriver_initializer import WebDriverInitializer
from utils.data_generator import *

logger = Logger(__name__)


@pytest.fixture(scope='class')
def browser(request) -> WebDriver:
    """Class-scoped browser fixture with setup/teardown to initialize the webdriver."""
    driver = None
    try:
        logger.info(f"\n{'='*50}\nStarting Setup Phase\n{'='*50}")
        driver = WebDriverInitializer().initialize_webdriver()
        driver.maximize_window()
        yield driver
    except Exception as e:
        logger.error(f'Failed to initialize WebDriver. Error: {e}')
    finally:
        if driver is not None:
            logger.info(f"\n{'='*50}\nStarting Teardown Phase\n{'='*50}")
            driver.quit()


@pytest.fixture(scope='session')
def register_data() -> dict:
    """Fixture that generates a dictionary of fake registration data."""
    password = generate_password()
    return {
        "first_name": generate_first_name(),
        "last_name": generate_last_name(),
        "address": generate_address(),
        "city": generate_city(),
        "state": generate_state(),
        "zip_code": generate_zipcode(),
        "phone": generate_phone_number(),
        "ssn": generate_ssn(),
        "username": generate_username(),
        "password": password,
        "confirm_password": password
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to handle test reports."""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('browser')
        if driver is not None:
            screenshots_dir = 'screenshots'
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f'{item.name}.png')
            try:
                driver.save_screenshot(screenshot_path)
                logger.info(f'Saved screenshot: {screenshot_path}')
            except WebDriverException as e:
                logger.error(f'Failed to save screenshot: {e}')
                raise WebDriverException('An error occurred while saving a screenshot')
            # attach to HTML report
            plugin = item.config.pluginmanager.getplugin("html")
            if plugin:
                extra = getattr(report, 'extra', [])
                html = (f'<div><img src="{screenshot_path}" alt="screenshot" style="width:300px;" '
                        f'onclick="window.open(this.src)" /></div>')
                extra.append(plugin.extras.html(html))
                report.extras = extra
