"""
Base page class for the ParaBank automation framework

@author: Raed Eleyan
@date: 04/10/2025
@contact: raedeleyan1@gmail.com
"""
import sys
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, WebDriverException, \
    NoAlertPresentException
from utils.logger import Logger

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))


class BasePage:
    """Base class for all page objects in the framework"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = Logger(__name__)

    def find_element(self, locator: tuple[str, str], timeout: int = 10) -> WebElement:
        """
        Finds and returns a single WebElement.

        :param locator: the locator strategy and value.
        :param timeout: the max time to wait for a WebElement to be visible. Default is 10 sec.
        :return: the WebElement.
        :raises TimeoutException: when the WebElement isn't found or not visible within the timeout.
        """
        try:
            self.logger.info(f'Locating a visible WebElement with locator: {locator}')
            web_element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f'Successfully located the WebElement with locator: {locator}')
            return web_element
        except TimeoutException as e:
            self.logger.error(f'Timeout! The WebElement with locator: {locator} not visible within {timeout} seconds.')
            raise TimeoutException(f"Visible WebElement not found: {locator}") from e

    def find_elements(self, locator: tuple[str, str], timeout: int = 10) -> list[WebElement]:
        """
        Finds and returns a list of WebElements.

        :param locator: the locator strategy and value.
        :param timeout: the max time to wait for a list of WebElements to be visible. Default is 10 sec.
        :return: a list of WebElements.
        :raises TimeoutException: when no WebElements are found or not visible within the timeout.
        """
        try:
            self.logger.info(f'Locating WebElements with locator: {locator}')
            web_elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            self.logger.info(f'Successfully located {len(web_elements)} WebElements with locator: {locator}')
            return web_elements
        except TimeoutException as e:
            self.logger.error(f'Timeout! No visible WebElements found with locator {locator} within {timeout} seconds.')
            raise TimeoutException(f'Visible WebElements not found: {locator}') from e

    def click(self, locator: tuple[str, str], timeout: int = 10) -> None:
        """
        Clicks on a WebElement after waiting for it to be present and clickable.

        :param locator: the locator strategy and value.
        :param timeout: the max time to wait for a WebElement to be clickable. Default is 10 sec.
        :raises TimeoutException: when a WebElement isn't found or not clickable within the timeout.
        """
        try:
            self.logger.info(f'Attempting to Click on a WebElement with locator: {locator}')
            web_element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            web_element.click()
            self.logger.info(f'Successfully clicked on the WebElement with locator: {locator}')
        except TimeoutException as e:
            self.logger.error(f'Timeout: WebElement {locator} not clickable within {timeout} seconds.')
            raise TimeoutException(f'WebElement not found or not clickable {locator}') from e

    def send_keys(self, locator: tuple[str, str], text: str) -> None:
        """
        Enters text into a WebElement after ensuring its visible and interactable.

        :param locator: the locator strategy and value.
        :param text: the text to enter into a WebElement.
        :raises TimeoutException: when the WebElement isn't found or not visible within the timeout.
        :raises ElementNotInteractableException: when the WebElement is present but not interactable.
        :raises WebDriverException: for other errors.
        """
        try:
            self.logger.info(f'Sending text "{text}" to a WebElement with locator: {locator}')
            web_element = self.find_element(locator)
            web_element.clear()
            web_element.send_keys(text)
            self.logger.info(f'Successfully sent text: "{text}" to the WebElement with locator: {locator}.')
        except TimeoutException as e:
            self.logger.error(f'Timeout! WebElement {locator} not found or not visible within timeout.')
            raise TimeoutException(f'Element not found or not visible: {locator}') from e
        except ElementNotInteractableException as e:
            self.logger.error(f'WebElement with locator: {locator} is present but not interactable.')
            raise ElementNotInteractableException(f'WebElement with locator: {locator} not interactable.') from e
        except WebDriverException as e:
            self.logger.critical(f'An error occurred while trying to send text "{text}" to WebElement with '
                                 f'locator: {locator}.')
            raise WebDriverException(f'Failed to send the text "{text}" to WebElement with this '
                                     f'locator: {locator}.') from e

    def switch_to_iframe(self, locator: tuple[str, str], timeout: int = 10) -> None:
        """
        Switches the WebDriver's context to the specified iframe.

        :param locator: the locator strategy and value.
        :param timeout: the max time to wait for the iframe to be available. Default is 10 sec.
        :raises TimeoutException: when the iframe is not available within the timeout.
        :raises WebDriverException: when an error occurs while trying to switch to iframe.
        """
        try:
            self.logger.info(f'Switching to iframe with locator: {locator}.')
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
            self.logger.info(f'Successfully switched to iframe with locator: {locator}.')
        except TimeoutException as e:
            self.logger.error(f'Timeout! iframe with {locator} not available within {timeout} seconds.')
            raise TimeoutException(f'iframe not available or not switchable: {locator}') from e
        except WebDriverException as e:
            self.logger.critical(f'An error occurred while trying to switch to iframe with locator: {locator}.')
            raise WebDriverException(f'Failed to switch to iframe with locator : {locator}.') from e

    def switch_to_default_content(self) -> None:
        """
        Switches the WebDriver's context back to the default content (outside all iframes   ).

        :raises WebDriverException: when an error occurs while trying to switch to the default content.
        """
        try:
            self.logger.info('Attempting to switch back to default content.')
            self.driver.switch_to.default_content()
            self.logger.info('Successfully switched back to the default content.')
        except WebDriverException as e:
            self.logger.critical('An error occurred while trying to switch back to the default content.')
            raise WebDriverException('Failed to switch back to the default content.') from e

    def accept_alert(self, timeout: int = 10) -> None:
        """
        Accepts an alert (clicks the "OK" button).

        :param timeout: the max time to wait for the alert to be present to accept. Default is 10 sec.
        :raises TimeoutException: when the alert is not present within the timeout.
        :raises NoAlertPresentException: when no alert is present to accept.
        :raises WebDriverException: when an error occurs while trying to accept an alert.
        """
        try:
            self.logger.info('Accepting an Alert.')
            alert = WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present()
            )
            alert.accept()
            self.logger.info('Successfully accepted the Alert.')
        except TimeoutException as e:
            self.logger.error(f'Timeout! Alert did not appear within {timeout} seconds.')
            raise TimeoutException(f'Alert not present after {timeout} seconds timeout.') from e
        except NoAlertPresentException as e:
            self.logger.error('Alert vanished before it could be accepted.')
            raise NoAlertPresentException('Alert disappeared before acceptance.') from e
        except WebDriverException as e:
            self.logger.critical('An error occurred while trying to accept the Alert.')
            raise WebDriverException('Failed to accept alert.') from e

    def dismiss_alert(self, timeout: int = 10) -> None:
        """
        Dismisses an alert (clicks the "Cancel" button).

        :param timeout: the max time to wait for the alert to be present to dismiss. Default is 10 seconds.
        :raises TimeoutException: when the alert is not present within the timeout.
        :raises NoAlertPresentException: when no alert is present to dismiss.
        :raises WebDriverException: when an error occurs while trying to dismiss an alert.
        """
        try:
            self.logger.info(f'Waiting up tp {timeout} seconds for alert to appear.')
            alert = WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present()
            )
            self.logger.debug('Alert detected. Attempting to dismiss alert.')
            alert.dismiss()
            self.logger.info('Successfully dismissed the Alert.')
        except TimeoutException as e:
            self.logger.error(f'Timeout! Alert not present within {timeout} seconds.')
            raise TimeoutException(f'No alert appeared in {timeout} seconds.') from e
        except NoAlertPresentException as e:
            self.logger.error('The Alert wasn\'t present.')
            raise NoAlertPresentException('No alert was present to dismiss.') from e
        except WebDriverException as e:
            self.logger.critical('An error occurred while trying to dismiss the Alert.')
            raise WebDriverException('Unable to dismiss the Alert.') from e

    def get_alert_text(self, timeout: int = 10) -> str:
        """
        Gets the text of an alert.

        :param timeout: the max time to wait for the alert to be present to get its text. Default is 10 seconds.
        :raises TimeoutException: when the alert is not present within the timeout.
        :raises NoAlertPresentException: when no alert is present to get its text.
        :raises WebDriverException: when an error occurs while trying to gett an alert text.
        """
        try:
            self.logger.info('Attempting to retrieve alert text.')
            alert = WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present()
            )
            self.logger.info('Successfully retrieved the text of the alert.')
            return alert.text
        except TimeoutException as e:
            self.logger.error(f'Timeout! Alert not found within {timeout} seconds.')
            raise TimeoutException(f'No alert appeared after {timeout} seconds wait') from e
        except NoAlertPresentException as e:
            self.logger.error('Alert vanished before text retrieval')
            raise NoAlertPresentException('Alert disappeared after detection.') from e
        except WebDriverException as e:
            self.logger.critical('An error occurred while trying to retrieve the text of the alert.')
            raise WebDriverException('Failed to get the alert text.') from e

    def send_keys_to_alert(self, text: str, timeout: int = 10) -> None:
        """
        Sends text to a prompt alert.

        :param text: the text to send.
        :param timeout: the max time to wait for the alert to be present to send keys to it. Default is 10 sec.
        :raises TimeoutException: when the alert is not present within the timeout.
        :raises NoAlertPresentException: when no alert is present to send keys to it.
        :raises WebDriverException: when an error occurs while trying to send keys to a prompt alert.
        """
        try:
            self.logger.info('Attempting to send text to prompt alert.')
            alert = WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present()
            )
            alert.send_keys(text)
            self.logger.info('Successfully sent text to prompt alert.')
        except TimeoutException as e:
            self.logger.error('Timeout! Prompt alert not found within {timeout} seconds.')
            raise TimeoutException(f'Text input prompt not present after {timeout} seconds') from e
        except NoAlertPresentException as e:
            self.logger.error('No prompt alert was present to send text to it.')
            raise NoAlertPresentException('Prompt disappeared before text could be entered') from e
        except WebDriverException as e:
            self.logger.critical('An error occurred while trying to send text to the prompt alert.')
            raise WebDriverException('Failed to send text to prompt alert.') from e
