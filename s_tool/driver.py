"""
Create Driver instance
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager


class SeleniumDriver:
    """
    driver class
    """

    def __init__(self, browser=None, headless=False, executable_path=None):
        self.browser = browser.lower()
        self.headless = headless
        self.executable_path = executable_path

    def load_driver(self):
        """
        Create and return webdriver instance
        """
        if self.browser == 'chrome':
            driver = self.get_chrome_driver()
        elif self.browser == 'firefox':
            driver = self.get_firefox_driver()
        elif self.browser == 'ie':
            driver = self.get_ie_driver()
        else:
            raise ValueError(f"Invalid browser: {self.browser}")

        return driver

    def get_chrome_driver(self):
        """
        Return chrome driver instance
        """
        driver = webdriver.Chrome(service=ChromeService(),
                                  options=self._get_chrome_options(),
                                  executable_path=self.executable_path or ChromeDriverManager().install())

        return driver

    def get_firefox_driver(self):
        """
        Return firefox driver instance
        """
        driver = webdriver.Firefox(options=self._get_firefox_options(),
                                   executable_path=self.executable_path or GeckoDriverManager().install())

        return driver

    def get_ie_driver(self):
        """
        Return firefox driver instance
        """
        driver = webdriver.Ie(service=IEService(),
                              options=self._get_ie_options(),
                              executable_path=self.executable_path or IEDriverManager().install())
        return driver

    def _get_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.headless = self.headless
        return options

    def _get_firefox_options(self):
        options = webdriver.FirefoxOptions()
        options.headless = self.headless
        return options

    def _get_ie_options(self):
        return webdriver.IeOptions()
