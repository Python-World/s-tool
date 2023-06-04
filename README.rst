**S-TOOL**

.. image:: https://user-images.githubusercontent.com/33047641/125023819-41998700-e09d-11eb-8076-7fad81f98f70.png
   :width: 150


``S-Tool`` is a utility module that provides helpful methods for interacting with Selenium WebDriver in Python

Installation
^^^^^^^^^^^^

Installation using PyPi
-----------------------

.. code:: bash

    pip install s-tool


Development Setup
-----------------

.. code:: bash

   # Clone this repository
    git clone https://github.com/Python-World/s-tool.git

    # Go into the repository
    cd sel-kit

    # Install dependencies
    poetry config virtualenvs.in-project true
    poetry install

    # Start Poetry shell
    poetry shell



Usage
^^^^^

* Example Using Context Manager

.. code-block:: python

      """Example code with context manager"""

      from s_tool.core import SeleniumDriver as SBot

      with SBot("firefox", headless=True) as self:
          self.get("https://google.com")
          sessionid = self.session()
          url = self.url()
          cookies = self.cookies()

          # print sessionid,url,cookies
          print(f"\nurl     :   {url} \nsession :   {sessionid}\ncookies :   {cookies}\n")


* Example Using class

.. code-block:: python 

    from s_tool.core import SeleniumTools

    class SBot(SeleniumTools):
        """Example Bot using s-tool"""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def run(self):
            """Code to visit url and fetch cookies and basic info"""
            url ="https://example.com"
            self.get(url)
            sessionid = self.sessionid()
            url = self.url()
            cookies = self.cookies()

            # print sessionid,url,cookies
            print(f"\nurl     :   {url} \nsession :   {sessionid}\ncookies :   {cookies}\n")


    bot = SBot(browser ="firefox", headless=True)  # change headless=False to run with gui mode
    bot.run()
    bot.close()


Methods
^^^^^^^

Here are the public methods available in the SeleniumTools class:
    - get(): Loads a web page with the specified URL or local file or Html Content.
    - url(): Returns the current URL of the page.
    - text(): Returns the source code of the current page.
    - get_driver_sessionid(): Return an session id string.
    - get_locator(): Returns a WebDriver locator based on the given element identifier and identifier type.
    - get_element(): Returns a single element or a list of elements matching the given element identifier and identifier type.
    - fill(): Fills in form elements with the provided values.
    - wait_for_element(): Waits for an element to be present and visible on the page.
    - element_visibility(): Toggles the visibility of an element on the page.
    - cookies(): Returns all cookies present in the current session.
    - set_cookies(): Sets cookies for the current session using a dictionary of cookie key-value pairs.
    - click(): Clicks on the element identified by the given element identifier and identifier type.
    - press_multiple_keys(): Presses multiple keys simultaneously using Selenium.
    - execute_script(): Executes JavaScript code in the context of the current page.
    - parse(): Parses the HTML content of the current page and returns a list of elements matching the given tag name and attribute value.
    


Feel free to refer to the documentation for each method to understand their parameters and usage.

Contributing
^^^^^^^^^^^^

Contributions are welcome! If you find any issues or have suggestions for improvement, please create an issue or submit a pull request.

License
-------
This project is licensed under the MIT License.