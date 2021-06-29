from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from s_tool.utils.driver_exceptions import SToolException


def get_session(driver):
    """Return Selenium Driver session id"""
    return driver.session_id


def visit(driver, url):
    """visit given url"""
    driver.get(url)


def page_source(driver):
    """Return html page source"""
    return driver.page_source


def current_url(driver):
    """Return current url"""
    return driver.current_url


def get_locator(locator_type, locator_text):
    """Return element locator

    Args:
        locator_type : provide any attribute type
                    id,class_name,tag_name
                    xpath, css_selector

        locator_text : attribute value
    """
    locator = locator_type.upper()
    return getattr(By, locator), locator_text


def get_element(driver, locator_type, locator_text, many=None):
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


def click(driver, locator_type, locator_text, click_time=10):
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


def get_cookies(driver):
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


def take_screenshot(driver, element=None):
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
        ele = get_element(driver, locator_type, locator_text)
        if ele:
            return ele.screenshot_as_png
        return None
    else:
        width = driver.execute_script("return document.body.offsetWidth")
        height = driver.execute_script("return document.body.offsetHeight")
        driver.set_window_size(width, height)
        return driver.get_screenshot_as_png()


def display_element(driver, element, hide=None):
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


def hide_show_elements(driver, elements, hide=None):
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
        element_list = get_element(driver, locator_type, locator_value, 1)
        if element_list:
            for element in element_list:
                display_element(driver, element, hide)
