from typing import Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from s_tool.exceptions import SToolException


def get_session(driver: webdriver) -> str:
    """Return Selenium Driver session id"""
    return driver.session_id


def visit(driver: webdriver, url: str) -> None:
    """visit given url"""
    driver.get(url)


def page_source(driver: webdriver) -> str:
    """Return html page source"""
    return driver.page_source


def current_url(driver: webdriver) -> str:
    """Return current url"""
    return driver.current_url


def get_locator(locator_type: str, locator_text: str) -> tuple:
    """Return element locator

    Args:
        locator_type : provide any attribute type
                    id,class_name,tag_name
                    xpath, css_selector

        locator_text : attribute value
    """
    locator = locator_type.upper()
    return getattr(By, locator), locator_text


def get_element(
    driver: webdriver, locator_text: str, locator_type: str = "id", many: bool = None
):
    """Get element using locator type and locator text

    Args:
        locator_type : provide any attribute type
                    id,class_name,tag_name
                    xpath, css_selector

        locator_text : attribute value

        many         : optional default None,
                       1: select multiple element
                       0: select single element

    Returns:
        Return an element object if found otherwise
        return None
    """

    locator_type = locator_type.upper()
    if hasattr(By, locator_type):
        try:
            locator = get_locator(locator_type, locator_text)
            is_multiple = "s" if many else ""
            func = getattr(driver, f"find_element{is_multiple}")
            return func(*locator)
        except NoSuchElementException:
            return None
    else:
        raise SToolException("INVALID_SELECTOR")


def click(
    driver: webdriver, locator_type: str, locator_text: str, click_time: int = 10
) -> Union[bool, None]:
    """Return True if element clicked otherwise return None

    Args:
        locator_type : provide any attribute type
                    id,class_name,tag_name
                    xpath, css_selector

        locator_text : attribute value

    Returns:
        True    : If element clicked
        None    : Not clicked or Not Found
    """
    try:
        elem_locator = get_locator(locator_type, locator_text)
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
    """Accept driver object and return cookies in dictionary

    Args:
        driver : A selenium WebDriver

    Returns:
        cookies_dict : return cookies in dicionary format if
                        no cookies return an empty dictionary
    """
    cookies = driver.get_cookies()
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
    return cookies_dict or {}


def take_screenshot(driver: webdriver, element: tuple = None) -> Union[bytes, None]:
    """take screenshot of given element if element is
    not given take a full page screeenshot and return
    data in bytes

    Args:
        driver  : selenium Webdriver
        element : default None, provide element locator
                example : element=('id','element_id')

    Returns:
        returns byte object,if element not present
        it will return None.

    full screenshot will work only in headless mode.
    """
    if element and isinstance(element, tuple):
        locator_type, locator_text = element
        ele = get_element(driver, locator_text, locator_type)
        if ele:
            return ele.screenshot_as_png
        return None
    else:
        width = driver.execute_script("return document.body.offsetWidth")
        height = driver.execute_script("return document.body.offsetHeight")
        driver.set_window_size(width, height)
        return driver.get_screenshot_as_png()


def display_element(driver: webdriver, element, hide=None) -> None:
    """hide or show single element

    Args:
        driver  : selenium webdriver
        element : an selenium element
        hide    : default value is None, to hide element
                    hide=1 to display hidden element
    Returns:
        None
    """

    hide_or_show = "inline" if hide else "None"
    driver.execute_script(f"arguments[0].style.display = '{hide_or_show}';", element)


def hide_show_elements(driver: webdriver, elements: list, hide: bool = None) -> None:
    """hide or show multiple elements

    Args:
        driver  : selenium webdriver
        elements  : list of tuples,[('locator_type','value')]
                example : [('id','id_value')]
        hide    : default value is None, to hide element
                 hide=1 to display hidden element

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
    """Select Dropdown option

    Args:
        element : selenium element
        _value  : str,value,text
        _by     : an int value from range(3)

                    0: default select option using by value
                    1: select using visible text
                    2: select using index but also provide _value as int
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


def fill(driver: WebDriver, kwargs: dict) -> None:
    """Fill information in html element using name attribute

    Args:
        driver : selenium Webdriver
        kwargs : dict,{name:value_to_select_or_enter}

        _by    : default 0 , used for select dropdown

    """

    for name, value in kwargs.items():
        element = get_element(driver, name, "name")
        if element.tag_name == "select":
            # Select Dropdown value
            select_option(element, value, _by=0)
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
