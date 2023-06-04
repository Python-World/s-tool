"""
SeleniumTools

"""

import inspect
import os
import string
import types
from typing import List, Optional, Type
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from .driver import SeleniumDriver
from .exceptions import InvalidWebDriverError, SToolException
from .logger import logger
from .parser import LxmlParser


class SeleniumTools:

    """
    A utility class for Selenium utilities functions.
    """

    def __init__(self, driver: webdriver = None, **kwargs) -> None:

        self.driver = driver

        self.browser = kwargs.get('browser')
        self.headless = kwargs.get('headless')
        self.executable_path = kwargs.get('exc_path')

        if 'parser' in kwargs:
            self._attach_custom_parsers(kwargs['parser'])
        self.parser = LxmlParser()

        if self._validate_driver() is False:
            self.driver = self._load_driver()

    def __exit__(self, typesa, value, tracebacks):
        """release the resources occupied with the current session

        Args:
            type ([type]): type
            value ([type]): value
            traceback ([type]): and traceback
        """
        if self._validate_driver() is True:
            self._close()

    def __enter__(self):
        """Returns an selenium webdriver
        Allows you to implement objects
        which can be used easily with the with statement

        Returns:
            [webDriver]: selenium webdriver
        """
        if self._validate_driver() is False:
            self.driver = self._load_driver()
            logger.info('selenium driver object created')

        return self

    def _load_driver(self):
        """Create Selenium webdriver object"""
        obj = SeleniumDriver(browser=self.browser,
                             headless=self.headless,
                             executable_path=self.executable_path)
        self.driver = obj.load_driver()

        return self.driver

    def _close(self):
        """will stop driver after program execution"""
        self.driver.close()
        print("selenium driver object closed")
        logger.info('selenium driver object closed')

    def _attach_custom_parsers(self, parser_class: Type) -> None:
        """
        Attaches custom parsers from the given parser class to the LxmlParser class.

        Args:
            parser_class (class): The parser class containing custom parsers.

        Example:
            # Create an instance of SeleniumTools
            MyCustomParser:
                def table(self,html_string,**kwargs):
                    ## process and return html string
                    processed_list = []
                    return processed_list

            selenium_tools = SeleniumTools(driver,parser_class=MyCustomParser)
        """

        source_methods = inspect.getmembers(
            parser_class(), predicate=inspect.ismethod)

        # Attach the methods to the source class
        for method_name, method_obj in source_methods:
            func = types.FunctionType(
                method_obj.__func__.__code__, globals(), method_name)
            setattr(LxmlParser, method_name, func)

    def parse(
            self,
            ele_tag: str,
            locator_text: str,
            locator_type: str = "id",
            **kwargs):
        """
        Parses an HTML element using the specified tag and locator.

        Args:
            ele_tag: str
                - The HTML tag to parse.
            locator_text: str
                - The locator text to find the HTML element.
            locator_type: str, optional
                - The locator type. Defaults to id.
            kwargs: dict
                - Additional keyword arguments to pass to the parser.

        Returns:
            object : objects
                - The parsed result.

        Raises:
            NotImplementedError: exception
                - If the parser for the specified tag is not implemented.

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Parse a table element by ID
            result = selenium_tools.parse("table", "table_id")

            # Parse a table with xpath
            result = selenium_tools.parse("table", "//table","xpath", attr1=value1)
        """
        final_result = []
        method = getattr(self.parser, ele_tag, None)
        if method is not None and callable(method):
            element = self.get_element(locator_text, locator_type)
            html_string = element.get_property('outerHTML')
            final_result = method(html_string, **kwargs)
        else:
            raise NotImplementedError(f"{ele_tag} parser not implemented")

        return final_result

    def _get_supported_browsers(self) -> List[str]:
        """
        Get a list of all supported browsers by Selenium.

        Returns:
            List[str]: A list of supported browsers.

        Example:
            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Get the supported browsers
            supported_browsers = selenium_tools._get_supported_browsers()

            print("Supported Browsers:", supported_browsers)
        """
        supported_browsers = [
            ele for ele in dir(webdriver) if 'webdriver' in dir(
                getattr(
                    webdriver, ele))]
        return supported_browsers

    def _validate_driver(self) -> None:
        """
        Validates the Selenium WebDriver by performing a basic operation.

        Raises:
            InvalidWebDriverError: If the input is not a valid Selenium WebDriver.

        Example:
            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Validate the driver
            selenium_tools._validate_driver()
        """
        err = "Selenium WebDriver validation failed."
        supported_browsers = self._get_supported_browsers()

        if hasattr(
                self.driver,
                'name') and self.driver.name not in supported_browsers:

            return False

        try:
            # Perform a basic operation to validate the driver
            self.driver.get('about:blank')  # Load a blank page
            # Check if the WebDriver is functioning properly
            if self.driver.title != '':
                raise InvalidWebDriverError(err)
            return True
        except InvalidWebDriverError:
            return False

    def sessionid(self) -> str:
        """
        Returns the session ID of the WebDriver instance.

        Returns:
            session_id : str
                - The session ID of the WebDriver instance.

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Get the session ID
            sessionid = selenium_tools.sessionid()

            print("Session ID:", sessionid)
        """
        # Return the session ID
        return self.driver.session_id

    def _is_valid_html(self, content: str) -> str:
        """
        Modifies the provided string based on its type
        (local file path, public URL, or HTML content).

        Args:
            content (str): The string content to modify.

        Returns:
            str: The modified string.

        Raises:
            ValueError: If the provided content is empty or not a valid string.
        """
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Invalid content. It must be a non-empty string.")

        parsed_url = urlparse(content)

        if os.path.exists(content):
            # Local file path
            if not content.startswith("file://"):
                content = "file://" + content

        elif parsed_url.scheme != '' and parsed_url.netloc != '':
            # Public URL, return as is
            return content
        else:
            # HTML content
            content = "data:text/html;charset=utf-8," + content

        return content

    def get(self, url_or_html: str) -> None:
        """
        Visits the given URL or local HTML file or html content using the Selenium WebDriver.

        Args:
            url: str
                - The URL or local HTML file path to visit.

        Raises:
            ValueError: If the URL is empty or not a valid string.

        Returns:
            None

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Visit a URL
            selenium_tools.visit("https://www.example.com")

            # Visit a local HTML file
            selenium_tools.visit("file:///path/to/local/file.html")
        """
        # Validate the URL or HTML content
        if not isinstance(url_or_html, str) or not url_or_html.strip():
            raise ValueError(
                "Invalid URL or HTML content. It must be a non-empty string.")

        # Check if it's HTML content
        content = self._is_valid_html(url_or_html)
        self.driver.get(content)

    def get_locator(
            self,
            locator_text: str,
            locator_type: str = "id") -> tuple:
        """
        Returns a locator tuple for the specified attribute value and locator type.

        Args:
            locator_text: str
                - The attribute value of the element.
            locator_type: str, optional
                - The type of locator to use (class_name, tag_name, xpath, css_selector)
                - Defaults to "id".

        Returns:
            key,val : tuple
                - A locator tuple in the format (By.locator, locator_value).

        Raises:
            ValueError: If the locator type is invalid.

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Get a locator for an element with ID 'myElement'
            locator = selenium_tools.get_locator('myElement', 'id')

            print("Locator:", locator)
        """
        # Validate the locator type
        valid_locator_types = [ele for ele in vars(
            By).keys() if not ele.startswith('__')]
        if locator_type.upper() not in valid_locator_types:
            raise ValueError(
                f"Invalid locator type. The locator type must be one of: {valid_locator_types}")

        locator = getattr(By, locator_type.upper())
        return locator, locator_text

    def click(
            self,
            locator_text: str,
            locator_type: str = "id",
            click_time: int = 10) -> bool:
        """
        Clicks on an element with the specified locator within the given Selenium WebDriver instance.

        Args:
            locator_text: str
                The attribute value of the element to click.

            locator_type: str, optional
                - The type of locator to use (class_name, tag_name, xpath, css_selector).
                - Defaults to "id".

            click_time: int, optional
                 - The maximum wait time in seconds for the element to be clickable.
                 - Defaults to 10.

        Returns:
            status: bool
                * True if the element is clicked successfully.
                * False if the element is not clicked within the specified time.

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Click on an element with ID 'myElement'
            success = selenium_tools.click('myElement', 'id')

            if success:
                print("Element clicked successfully.")
            else:
                print("Element click failed.")
        """
        try:

            elem_locator = self.get_locator(locator_text, locator_type)

            element = WebDriverWait(
                self.driver, click_time).until(
                EC.element_to_be_clickable(elem_locator))
            element.click()
            logger.info(
                "clicked on value:%s attribute:%s",
                locator_text,
                locator_type)
            return True
        except TimeoutException:
            return False

    def get_element(self,
                    locator_text: str,
                    locator_type: str = "id",
                    many: Optional[bool] = None) -> Optional[List[WebElement]]:
        """
        Returns an element or a list of elements using the specified
        locator type and text.

        Args:
            locator_text: str
                - The attribute value of the element to locate.

            locator_type: str, optional
                - The type of locator to use (class_name, tag_name, xpath, css_selector)
                - Defaults to "id".

            many: bool, optional
                - Returns a list of elements if True,
                - returns a single element if False or None.
                - Defaults to None.

        Raises:
            SToolException: If an invalid selector is provided.

        Returns:
            element :  [List[WebElement]]
                - A list of elements if many=True.
                - A single element if many=False or None.
                - None if the element is not found.

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Get a single element by ID
            element = selenium_tools.get_element('myElement', 'id', many=False)

            # Get multiple elements by class name
            elements = selenium_tools.get_element('myClass', 'class_name', many=True)
        """
        locator_type = locator_type.upper()
        if hasattr(By, locator_type):
            try:
                locator = self.get_locator(locator_text, locator_type)
                elements = None
                if many:
                    elements = self.driver.find_elements(*locator)
                else:
                    elements = self.driver.find_element(*locator)

                return elements
            except NoSuchElementException as exc:
                raise NoSuchElementException(locator_text) from exc
        else:
            raise SToolException("INVALID_SELECTOR")

    def select_option(
            self,
            element: WebElement,
            _value: str,
            _by: int = 0) -> None:
        """
        Selects a dropdown option based on the specified criteria.

        Args:
            element: WebElement
                - The Selenium WebElement representing the dropdown element.
            _value: str
                - The value, text, or index to select the option by.

            _by: int, optional
                - The selector type. Defaults to 0.
                - 0: Select the option by value.
                - 1: Select the option by visible text.
                - 2: Select the option by index (requires _value to be an integer).

        Raises:
            * SToolException: If the element is not a select (dropdown) element.
            * SToolException: If an invalid selector is provided.
            * SToolException: If an invalid value is provided when selecting by index.

        Returns:
            None

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Assuming `dropdown_element` is a WebElement representing a dropdown
            # Select an option by value
            selenium_tools.select_option(dropdown_element, 'option_value', _by=0)

            # Select an option by visible text
            selenium_tools.select_option(dropdown_element, 'Option Text', _by=1)

            # Select an option by index
            selenium_tools.select_option(dropdown_element, 2, _by=2)
        """

        # Validate if element is a select element
        if not element or element.tag_name != "select":
            raise SToolException("INVALIDELEMENT")

        # Validate the selector type
        if _by not in [0, 1, 2]:
            raise SToolException("INVALIDSELECTOR")

        # Validate the value when selecting by index
        if _by == 2 and not isinstance(_value, int):
            raise SToolException("INVALIDVALUE")

        # Select the option based on the selector type
        select = Select(element)
        select_type = {
            0: select.select_by_value,
            1: select.select_by_visible_text,
            2: select.select_by_index,
        }

        select_type[_by](_value)

    def fill(self, kwargs: dict, _by: int = 0) -> None:
        """
        Inserts or selects values using the specified criteria
        for a collection of form elements.

        Args:

            kwargs: dict

                - A dictionary containing the form elements as keys and their corresponding values or options as values.

            _by: int, optional

                - The selector type. Defaults to 0.
                - 0: Select the option by value (for dropdown elements).
                - 1: Select the option by visible text (for dropdown elements).
                - 2: Select the option by index (for dropdown elements).

        Raises:
            SToolException: If an invalid selector is provided.
            SToolException: If an invalid value is provided when selecting by index.

        Returns:
            None

        Example:

        .. code-block:: python

            # Create an instance of SeleniumTools
            selenium_tools = SeleniumTools(driver)

            # Assuming `form_elements` is a dictionary of form elements and their values
            # Fill in form elements
            selenium_tools.fill(form_elements)

            # Fill in form elements using index selector
            selenium_tools.fill(form_elements, _by=2)
        """

        # Validate the selector type
        if _by not in [0, 1, 2]:
            raise SToolException("INVALIDSELECTOR")

        for element, value in kwargs.items():
            web_element = self.get_element(element, 'name', many=False)
            if not web_element:
                raise NoSuchElementException("value:{element} attribute:name")

            if isinstance(value, str):
                web_element.clear()
                web_element.send_keys(value)
            elif isinstance(value, (int, bool, float)):
                web_element.clear()
                web_element.send_keys(str(value))
            elif isinstance(value, list):
                self.select_option(web_element, value, _by=_by)
            else:
                raise SToolException("INVALIDVALUE")

    def press_multiple_keys(self, keys: list):
        """
        Presses multiple keys simultaneously using Selenium.

        Args:
            keys:list
                - A list of keys to press.

        Raises:
            ValueError: If any of the keys are not valid.

        Example usage:

        .. code-block:: python

            selenium_tools = SeleniumTools(driver)
            keys_to_press = ['CTRL','SHIFT','A']  # Example: Pressing CTRL+SHIFT+A
            selenium_tools.press_multiple_keys(keys_to_press)
        """

        valid_non_modifier_keys = string.ascii_uppercase
        keys = [key.upper() for key in keys]

        # Validate the keys
        for key in keys:
            if not isinstance(key, str) and key not in vars(
                    Keys).values() and key not in valid_non_modifier_keys:
                raise ValueError(
                    f"Invalid key: {key}. Keys must be either strings, valid keys from the Keys class, or valid non-modifier keys.")

        # Create an ActionChains object
        action_chains = ActionChains(self.driver)

        # Press each key in the list
        for key in keys:
            if isinstance(key, str):
                if key in valid_non_modifier_keys:
                    action_chains.send_keys(key)
                else:
                    key = getattr(Keys, key)
            action_chains.key_down(key)

        # Release each key in reverse order
        for key in reversed(keys):
            if isinstance(key, str):
                if key in valid_non_modifier_keys:
                    action_chains.send_keys(key)
                else:
                    key = getattr(Keys, key)
            action_chains.key_up(key)

        # Perform the actions
        action_chains.perform()

    def cookies(self) -> dict:
        """
        Returns the cookies of the given Selenium WebDriver instance as a dictionary.

        Returns:
            cookies_dict :dict
                - The cookies as a dictionary.
                - If no cookies are present,an empty dictionary is returned.

        Example:

        .. code-block:: python

            selenium_tools = SeleniumTools(driver)
            cookies = selenium_tools.cookies()
            print(cookies)
        """

        cookies = self.driver.get_cookies()
        cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
        return cookies_dict or {}

    def set_cookies(
            self,
            drop_all: bool = False,
            drop_keys: None = None,
            **cookies) -> None:
        """
        Adds cookies to the given Selenium WebDriver instance.

        Args:
            drop_all: bool, optional
                - If True, delete all cookies before adding the new ones.
                - Defaults to False.
            drop_keys: list, optional
                - A set of cookie names to be deleted before adding the new ones.
                - Defaults to an none.

            cookies:
                - Keyword arguments representing the cookies to be added.
                - Each keyword argument should be in the format 'name=value'.

        Returns:
            None

        Example:

        .. code-block:: python

            selenium_tools = SeleniumTools(driver)
            selenium_tools.set_cookies(drop_all=True, cookie1='value1', cookie2='value2')
        """

        # Convert cookie names and values to strings
        cookie = {str(k): str(v) for k, v in cookies.items()}

        # Delete all cookies if specified
        if drop_all:
            self.driver.delete_all_cookies()

        # Delete specific cookies by name
        drop_keys = drop_keys if drop_keys else []
        for name in drop_keys:
            self.driver.delete_cookie(name)

        # Add new cookies
        for name, value in cookie.items():
            self.driver.add_cookie({"name": name, "value": value})

    def execute_js(self, statement: str) -> str:
        """
        Execute a JavaScript statement using the given
        Selenium WebDriver instance and return the output.

        Args:
            statement: str
                - The JavaScript statement or variable name to run.

        Raises:
            ValueError: If the statement is not a valid string.

        Returns:
            result :str
                - The console output of the executed js statement in string format.

        Example:

        .. code-block:: python

            selenium_tools = SeleniumTools(driver)
            url = selenium_tools.execute_js("document.URL")
            print("Current URL:", url)

        """
        # Validate the statement
        if not isinstance(statement, str) or not statement.strip():
            raise ValueError(
                "Invalid statement. The statement must be a non-empty string.")

        if not statement.startswith('return'):
            statement = "return " + statement

        # Execute the JavaScript statement and return the output
        return str(self.driver.execute_script(statement))

    def text(self) -> str:
        """
        Returns the HTML source code of the currently loaded page
        in the given Selenium WebDriver instance.

        Raises:
            ValueError: If the driver is not a valid WebDriver instance.

        Returns:
            html_string: str
                - The HTML source code of the currently loaded page.

        Example:

        .. code-block:: python

            selenium_tools = SeleniumTools(driver)
            source = selenium_tools.page_source()
            print("Page Source:", source)
        """
        # Return the page source
        return self.driver.page_source

    def url(self) -> str:
        """
        Returns the current loaded URL in the given Selenium WebDriver instance.

        Returns:
            url :str
                - The current loaded URL.

        Example:

        .. code-block:: python

            selenium_tools = SeleniumTools(driver)
            url = selenium_tools.url()
            print("Current URL:", url)
        """

        return self.driver.current_url

    def wait_for_element(self, locator_text, locator_type='id', timeout=10):
        """
        Waits for an element to be present and visible on the page.

        Args:
            locator_text:str
                - The text of the locator.
            locator_type: str
                - The type of locator to use (default: 'id').
            timeout : int
                - The maximum time in seconds to wait for the element (default: 10).

        Raises:
            TimeoutException: If the element is not found within the specified timeout.

        Returns:
            element : WebElement
                - The found element.

        Example Usage:

        .. code-block:: python

            selenium_tool = SeleniumTool(driver)
            try:
                # Wait for an element with id 'my_element' to be present and visible
                element = selenium_tool.wait_for_element('my_element', 'id')

                # Perform actions on the element
                element.click()
            except TimeoutException:
                print("Element not found within the specified timeout.")
        """
        try:
            locator = self.get_locator(locator_text, locator_type)
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException as exc:
            raise TimeoutException(
                f"Element with locator '{locator_type}={locator_text}' was not found within {timeout} seconds.") from exc

    def element_visibility(
            self,
            element: WebElement,
            hide: bool = True) -> None:
        """
        Toggles the visibility of an element on the page.

        Args:
            element: WebElement
                The WebElement object representing the element to be toggled.

            hide: bool, optional
                - Determines whether to hide the element.
                - If True (default), the element will be hidden.
                - If False,the element will be shown.

        Example usage:

         .. code-block:: python

            selenium_tools = SeleniumTools(driver)

            # Wait for an element to be present
            element = selenium_tools.wait_for_element("//div[@id='myElement']")

            # Hide the element
            selenium_tools.element_visibility(element, hide=True)

            # Show the element
            selenium_tools.element_visibility(element, hide=False)
        """
        display_value = 'none' if hide else 'block'
        self.driver.execute_script(
            f"arguments[0].style.display = '{display_value}';", element)


if __name__ == '__main__':
    pass
