from functools import partial

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.utils import ChromeType

from s_tool.exceptions import SToolException
from s_tool.utils import (
    click,
    current_url,
    fill,
    get_cookies,
    get_element,
    get_session,
    get_user_agent,
    hide_show_elements,
    is_element,
    page_source,
    set_cookies,
    take_screenshot,
    visit,
)


class Browser:
    """Available Browser list"""

    CHROME = "chrome"
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    IE = "ie"


class SeleniumDriver:
    """SeleniumDriver class to manage driver object and all utility functions at one place"""

    def __init__(self, browser=None, headless=False, executable_path=None):

        self.browser_list = ["chrome", "chromium", "firefox", "ie"]
        self.driver = None
        self.browser = browser
        self.headless = headless
        self.executable_path = executable_path

        self._load_driver()
        self._load_methods()

    def close(self):
        """will stop driver after program execution"""
        if self.driver:
            self.driver.quit()

    def __exit__(self, type, value, traceback):
        """release the resources occupied with the current session

        Args:
            type ([type]): type
            value ([type]): value
            traceback ([type]): and traceback
        """
        self.close()

    def __enter__(self):
        """Returns an selenium webdriver
        Allows you to implement objects
        which can be used easily with the with statement

        Returns:
            [webDriver]: selenium webdriver
        """
        return self._load_driver()

    def _exe_path(self, manager, **params):
        """Return Webdriver path

        Args:
            manager ([ChromeDriver,GeckoDriver,IEDriver]): WebDriver Manager

        Returns:
            [str]: return an executable path
        """
        if self.executable_path:
            return self.executable_path
        else:
            return manager(**params).install()

    def _browser(self, browser):
        """Return if an valid browser passed

        Args:
            browser ([Browser]): Browser Type

        Returns:
            [bool]: True if browser is valid
        """
        available = False
        if self.browser.lower() == browser:
            available = True

        return available

    def _load_driver(self):
        """Create Selenium webdriver object"""
        self.close()
        browser = self.browser.lower()
        func = partial(self._exe_path)

        # Add Browser Options
        browser_options = browser if browser != Browser.CHROMIUM else Browser.CHROME
        options = getattr(webdriver, browser_options).options.Options()

        if self.headless:
            options.add_argument("--headless")

        if self._browser(Browser.CHROME):
            exe_path = func(ChromeDriverManager, chrome_type=ChromeType.GOOGLE)
            _webdriver = webdriver.Chrome

        elif self._browser(Browser.CHROMIUM):
            exe_path = func(ChromeDriverManager, chrome_type=ChromeType.CHROMIUM)
            _webdriver = webdriver.Chrome

        elif self._browser(Browser.FIREFOX):
            exe_path = func(GeckoDriverManager)
            _webdriver = webdriver.Firefox

        elif self._browser(Browser.IE):
            exe_path = func(IEDriverManager)()
            _webdriver = webdriver.Ie

        else:
            err = f"browser not implemented. available browers :{self.browser_list}"
            raise SToolException(err)

        self.driver = _webdriver(executable_path=exe_path, options=options)

        # Maximize window to give normal browser feel
        self.driver.maximize_window()

        # Load all modules and methods
        self._load_methods()

        return self

    def _load_methods(self):
        """Load basic methods"""
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
        self.is_element = partial(is_element, self.driver)
        self.set_cookies = partial(set_cookies, self.driver)
        self.ua = partial(get_user_agent, self.driver)


if __name__ == "__main__":
    pass
