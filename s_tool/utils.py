from typing import Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from s_tool.exceptions import SToolException


def get_session(driver: webdriver) -> str:
    """Return webdriver session

    Args:
        driver (webdriver): selenium webdriver

    Returns:
        str: sample '41ecb942-cd73-4407-aadd-acc7b8fbcd47
    """
    return driver.session_id


def is_local(path: str) -> str:
    """Return valid URL path for file

    Args:
        path (str): normal path or URL

    Returns:
        str: Modified file path if local file
            Returns path as it is if URL
    """
    import os

    URL = path
    if os.path.exists(path) or path.startswith("file"):
        if not URL.startswith("file"):
            URL = f"file://{URL}"
    return URL


def visit(driver: webdriver, url: str) -> None:
    """Visit given url

    Args:
        driver (webdriver): selenium webdriver
        url (str): [description]

    Returns:
        None
    """
    driver.get(is_local(url))


def page_source(driver: webdriver) -> str:
    """Return html page source which is rendered

    Args:
        driver (webdriver): selenium webdriver

    Returns:
        str: an html string
    """
    return driver.page_source


def current_url(driver: webdriver) -> str:
    """Returns Current loaded url

    Args:
        driver (webdriver): selenium webdriver

    Returns:
        str: An URL
    """
    return driver.current_url


def get_locator(locator_text: str, locator_type: str = "id") -> tuple:
    """Return an locator value

    Args:
        locator_text (str): attribute value
        locator_type (str, optional): provide any attribute type.If not provided id will use

    Returns:
        tuple: a locator value (By.locator,locator_value)
    """
    locator = locator_type.upper()
    return getattr(By, locator), locator_text


def get_element(
    driver: webdriver, locator_text: str, locator_type: str = "id", many: bool = None
):
    """Return element using locator type and text

    Args:
        driver (webdriver): selenium webdriver
        locator_text (str): attribute value
        locator_type (str, optional): attribute name. Defaults to "id".
                                    id,class_name,tag_name,xpath,css_selector
        many (bool, optional): Returns multiple element if True. Defaults to None.

    Raises:
        SToolException: If INVALID_SELECTOR provided

    Returns:
        [list,None]: Returns list of element if many=True
                    Else Return Single element
                    Return None If Element not Found
    """

    locator_type = locator_type.upper()
    if hasattr(By, locator_type):
        try:
            locator = get_locator(locator_text, locator_type)
            is_multiple = "s" if many else ""
            func = getattr(driver, f"find_element{is_multiple}")
            return func(*locator)
        except NoSuchElementException:
            return None
    else:
        raise SToolException("INVALID_SELECTOR")


def click(
    driver: webdriver, locator_text: str, locator_type: str = "id", click_time: int = 10
) -> Union[bool, None]:
    """[summary]

    Args:
       driver (webdriver): selenium webdriver
        locator_text (str): attribute value
        locator_type (str, optional): attribute name. Defaults to "id".
                                    id,class_name,tag_name,xpath,css_selector
        click_time (int, optional): time to wait till element is clickable. Defaults to 10.

    Raises:
        SToolException: [description]

    Returns:
        Union[bool, None]: True if element is clicked
                           False if element not clicked
    """
    try:
        elem_locator = get_locator(locator_text, locator_type)
        element = WebDriverWait(driver, click_time).until(
            EC.element_to_be_clickable(elem_locator)
        )
        element.click()
        return True
    except TimeoutException:
        return None
    except Exception as ex:
        raise SToolException(ex)


def get_cookies(driver: webdriver) -> dict:
    """Return cookies in dictionary

    Args:
        driver (webdriver): selenium webdriver

    Returns:
        dict: return cookies in dicionary,
              will return {} if no cookies
    """

    cookies = driver.get_cookies()
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
    return cookies_dict or {}


def set_cookies(
    driver: webdriver,
    drop_all: bool = False,
    drop_keys: set = set(),
    **cookies,
) -> None:
    """Add cookies into driver

    Args:
        driver (webdriver): selenium webdriver
        drop_all (bool, optional): Delete all cookies if True. Defaults to False.
        drop_keys (set, optional): Set of cookies name. Defaults to set().

    Returns:
        None
    """

    # cookies name and value must be in string
    cookies = {str(k): str(v) for k, v in cookies.items()}

    # Delete all cookies
    if drop_all:
        driver.delete_all_cookies()

    # Delete only given cookies Name
    for name in drop_keys:
        driver.delete_cookie(name)

    # Add new cookies
    for name, value in cookies.items():
        driver.add_cookie({"name": name, "value": value})


def take_screenshot(driver: webdriver, element: tuple = None) -> Union[bytes, None]:
    """Return screenshot

    Args:
        driver (webdriver): selenium webdriver
        element (tuple, optional): provide element locator
                            example : element=('id','element_id').
                            Defaults to None.

    Returns:
        Union[bytes, None]: Returns screenshot object
    """
    if element and isinstance(element, tuple):
        locator_type, locator_text = element
        ele = get_element(driver, locator_text, locator_type)
        if ele:
            return ele.screenshot_as_png
        return None
    else:
        width = driver.execute_script("return document.body.parentNode.scrollWidth")
        height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size(width, height)
        return driver.get_screenshot_as_png()


def display_element(driver: webdriver, element, hide: bool = None) -> None:
    """Hide and display element

    Args:
        driver (webdriver): selenium webdriver
        element ([selenium]): an selenium element
        hide (bool, optional): will display element if True. Defaults to None.

    Returns:
        None
    """

    hide_or_show = "inline" if hide else "None"
    driver.execute_script(f"arguments[0].style.display = '{hide_or_show}';", element)


def hide_show_elements(driver: webdriver, elements: list, hide: bool = None) -> None:
    """Hide and display elements

    Args:
        driver (webdriver): selenium webdriver
        elements (list): an list of element locator
                        [('locator_type','value')]
                        example : [('id','id_value')]
        hide (bool, optional): display elements if 'True' else Hide elements. Defaults to None.

    Returns:
        None
    """
    for element_locator in elements:
        locator_type, locator_value = element_locator
        element_list = get_element(driver, locator_value, locator_type, many=True)
        if element_list:
            for element in element_list:
                display_element(driver, element, hide)


def select_option(element, _value, _by=0):
    """select dropdown option

    Args:
        element ([type]): selenium element
        _value ([type]): str,value,text
        _by (int, optional): selector type, int. Defaults to 0.
                    0: default select option using by value
                    1: select using visible text
                    2: select using index but also provide _value as int

    Raises:
        SToolException: INVALIDELEMENT,if element is not select(dropdown)
        SToolException: INVALIDSELECTOR, wrong selector provided
        SToolException: INVALIDVALUE, for select_by_index second parameter required only integer

    Returns:
        None
    """

    if not element and element.tag_name != "select":
        raise SToolException("INVALIDELEMENT")

    elif _by not in [0, 1, 2]:
        raise SToolException("INVALIDSELECTOR")

    elif _by == 2 and type(_value) is not int:
        raise SToolException("INVALIDVALUE")

    else:
        select = Select(element)
        select_type = {
            0: getattr(select, "select_by_value"),
            1: getattr(select, "select_by_visible_text"),
            2: getattr(select, "select_by_index"),
        }

        select_type[_by](_value)


def fill(driver: WebDriver, kwargs, _by=0):
    """Insert or select values using name attribute

    Args:
        driver (WebDriver): selenium webdriver
        kwargs (dict): name and values in dict
                    example: {name:value_to_select_or_enter}
        _by    : Selector type, Default 0

    Raises:
        SToolException: NOTIMPLEMENTED,if html elment is not defined

    Returns:
        None
    """

    for name, value in kwargs.items():
        element = get_element(driver, name, "name")
        if element.tag_name == "select":
            # Select Dropdown value
            select_option(element, value, _by=_by)
        elif element.get_attribute("type") == "radio":
            # Click on radio element using value
            radio_element = get_element(driver, f'//input[@value="{value}"]', "xpath")
            radio_element.click()
        elif element.tag_name == "input":
            # input,textarea add values
            element.clear()
            element.send_keys(value)
        else:
            raise SToolException("NOTIMPLEMENTED")


def is_element(
    driver: WebDriver, locator_text: str, locator_type: str = "id", wait_time: int = 2
) -> bool:
    """Check element is loaded on page or not

    Args:
        driver (WebDriver): selenium webdriver
        locator_text (str): attribute value
        locator_type (str, optional): attribute name. Defaults to "id".
                                    id,class_name,tag_name,xpath,css_selector
        wait_time (int, optional): wait time to load element if not loaded. Defaults to 2.

    Returns:
        [bool]: True if element available, else False
    """

    try:
        locator = get_locator(locator_text, locator_type)
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(locator))
        return True
    except:
        return False


def get_user_agent(driver: webdriver) -> str:
    """Return user agent

    Args:
        driver (webdriver): selenium webdriver

    Returns:
        str: an user agent string.
    """

    return driver.execute_script("return navigator.userAgent")
