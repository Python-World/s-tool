from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from utils.driver_exceptions import SToolException


def get_session(driver):
    """Return Selenium Driver session id
    """
    return driver.session_id


def visit(driver, url):
    """visit given url 
    """
    driver.get(url)


def page_source(driver):
    """Return html page source
    """
    return driver.page_source


def current_url(driver):
    """Return current url
    """
    return driver.current_url


def get_locator(locator_type, locator_text):
    """Return element locator

    Args:
        locator_type : provide any attribute type
                    id,class_name,tag_name
                    xpath, css_selector

        locator_text : attribute value
    """
    return getattr(By, locator_type), locator_text


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
            is_multiple = 's' if many else ''
            func = getattr(driver, f'find_element{is_multiple}')
            return func(*locator)
        except NoSuchElementException as _:
            return None
    else:
        raise SToolException("INVALID_SELECTOR")
