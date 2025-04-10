"""
Pytest configuration and fixtures for ParaBank automation framework

@author: Raed Eleyan
@date: 04/10/2025
@contact: raedeleyan1@gmail.com
"""
import sys
import pytest
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from utils.logger import Logger
from utils.webdriver_initializer import WebDriverInitializer


logger = Logger(__name__)


@pytest.fixture(scope='class')
def browser(request) -> WebDriver:
    """Class-scoped browser fixture with setup/teardown to initialize the webdriver."""
    driver = None
    try:
        logger.info(f"\n{'='*50}\nStarting Setup Phase\n{'='*50}")
        driver = WebDriverInitializer().initialize_webdriver()
        driver.maximize_window()
        request.cls.driver = driver
        yield
    except Exception as e:
        logger.error(f'Failed to initialize WebDriver. Error: {e}')
    finally:
        logger.info(f"\n{'='*50}\nStarting Teardown Phase\n{'='*50}")
        driver.quit()
