from functools import partial

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.utils import ChromeType

from s_tool.exceptions import SToolException
from s_tool.utils import (
    click,
    current_url,
    fill,
    get_cookies,
    get_element,
    get_session,
    hide_show_elements,
    page_source,
    take_screenshot,
    visit,
)


class SeleniumDriver:
    """SeleniumDriver class to manage driver object and all utility functions at one place"""

    def __init__(self, browser=None, headless=False):
        self.browser_list = ["chrome", "chromium", "firefox"]
        self.driver = None
        self.browser = browser
        self.headless = headless

        self._load_driver()
        self._load_methods()

    def close(self):
        """will stop driver after program execution"""
        if self.driver:
            self.driver.quit()

    def __exit__(self, type, value, traceback):
        """release the resources occupied with the current session"""
        self.close()

    def __enter__(self):
        return self._load_driver()

    def _load_driver(self):
        """Create Selenium webdriver object"""
        self.close()
        browser = self.browser.lower()
        if browser not in self.browser_list:
            raise SToolException(
                f"provided browser {browser} doesn't exists. available brower list:{self.browser_list}"
            )

        # add chrome and firefox different options
        options = getattr(
            webdriver, browser if browser != "chromium" else "chrome"
        ).options.Options()
        if self.headless:
            options.add_argument("--headless")

        if browser in ["chrome", "chromium"]:
            browser_type = (
                ChromeType.CHROMIUM if browser == "chromium" else ChromeType.GOOGLE
            )
            self.driver = webdriver.Chrome(
                ChromeDriverManager(chrome_type=browser_type).install(), options=options
            )

        if browser == "firefox":
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install(), options=options
            )

        # Maximize window to give normal browser feel
        self.driver.maximize_window()

        # Load all modules and methods
        self._load_methods()

        return self

    def _load_methods(self):
        self.session = partial(get_session, self.driver)
        self.get = partial(visit, self.driver)
        self.text = partial(page_source, self.driver)
        self.url = partial(current_url, self.driver)
        self.element = partial(get_element, self.driver)
        self.click = partial(click, self.driver)
        self.cookies = partial(get_cookies, self.driver)
        self.screenshot = partial(take_screenshot, self.driver)
        self.hide = partial(hide_show_elements, self.driver)
        self.fill = partial(fill, self.driver)


if __name__ == "__main__":
    pass
