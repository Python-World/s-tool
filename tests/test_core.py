
import os
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from s_tool.core import SeleniumTools


class LXMLParser:
    def link(self,html_string,**kwargs):
        from lxml.html import fromstring
        etree = fromstring(html_string)
        links = etree.xpath('//a')[0].values() 
        return links


class SeleniumToolsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.

        cls.driver = webdriver.Chrome(chrome_options=options,service=ChromeService(ChromeDriverManager().install()))
        cls.selenium_tools = SeleniumTools(driver=cls.driver,parser=LXMLParser)
        cls.url = "https://www.example.com/"
        cls.example_file =os.path.join(os.path.dirname(__file__),'data/example.html')
        cls.selenium_tools.get(cls.url)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_get_supported_browsers(self):
        supported_browsers = self.selenium_tools._get_supported_browsers()
        self.assertIsInstance(supported_browsers, list)
        self.assertGreater(len(supported_browsers), 0)

    def test_sessionid(self):
        session_id = self.selenium_tools.sessionid()
        self.assertIsInstance(session_id, str)
        self.assertGreater(len(session_id), 0)

    def test_get(self):
        ## public url
        self.selenium_tools.get(self.url)
        self.assertEqual(self.driver.current_url, self.url)

    def test_get_local_file(self):
        ## public url
        self.selenium_tools.get(self.example_file)
        self.assertTrue(self.driver.current_url.startswith('file://'))
        self.selenium_tools.get(self.url) ## setting back original url

    def test_get_html_content(self):
        ## public url
        self.selenium_tools.get(open(self.example_file).read())
        self.assertTrue(self.driver.current_url.startswith('data'))
        self.selenium_tools.get(self.url) ## setting back original url

    def test_parse(self):
        expected_result =['https://www.iana.org/domains/example']

        links = self.selenium_tools.parse('link','//a','xpath')
        self.assertEqual(links,expected_result)
      

    
    def test_url(self):
        url = self.selenium_tools.url()
        self.assertEqual(url,self.url)
    
    def test_text(self):
        text  = self.selenium_tools.text()
        self.assertTrue(isinstance(text,str))
    
    def test_execute_js(self):
        url = self.selenium_tools.execute_js("document.URL") 
        self.assertEqual(url, self.url)

    def test_get_locator(self):
        locator_text = "myElement"
        locator_type = "id"
        locator = self.selenium_tools.get_locator(locator_text, locator_type)
        self.assertIsInstance(locator, tuple)
        self.assertEqual(len(locator), 2)
        self.assertEqual(locator[0], By.ID)
        self.assertEqual(locator[1], locator_text)

    def test_click(self):
        locator_text = "//a"
        locator_type = "xpath"
        success = self.selenium_tools.click(locator_text, locator_type)
        self.assertTrue(success)
        # Check if the element is clicked by asserting some condition
        self.selenium_tools.get(self.url)

    def test_get_element(self):
        locator_text = "//a"
        locator_type = "xpath"
        element = self.selenium_tools.get_element(locator_text, locator_type, many=False)
        self.assertIsInstance(element, WebElement)
        # Check if the element is found by asserting some condition

    def test_press_multiple_keys(self):
        keys_to_press = ['CONTROL','P']
        self.selenium_tools.press_multiple_keys(keys_to_press)
        # Check if the keys are pressed by asserting some condition

    def test_cookies(self):
        cookies = self.selenium_tools.cookies()
        self.assertIsInstance(cookies, dict)
        # Check if the cookies are retrieved by asserting some condition

    def test_set_cookies(self):
        # Assuming `cookies` is a dictionary of cookies
        cookies = {"name": "value", "foo": "bar"}
        self.selenium_tools.set_cookies(**cookies)

        # Check if the cookies are set by asserting some condition
        new_cookies = self.selenium_tools.cookies()
        self.assertEqual(new_cookies,cookies)
    
    def test_wait_for_element(self):
        try:
            self.selenium_tools.wait_for_element("invalid_element","name")
        except Exception as exc:
            self.assertTrue('name=invalid_element' in str(exc))
    
    def test_element_visibility(self):
        # Wait for an element to be present
        element = self.selenium_tools.wait_for_element('//h1[.="Example Domain"]','xpath')

        # Hide the element
        self.selenium_tools.element_visibility(element, hide=True)
        self.assertFalse(element.is_displayed())
        
        # Show the element
        self.selenium_tools.element_visibility(element, hide=False)
        self.assertTrue(element.is_displayed())

if __name__ == "__main__":
    unittest.main()
