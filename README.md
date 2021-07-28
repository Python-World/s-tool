# S-Tool

![S-tool](https://user-images.githubusercontent.com/33047641/125023819-41998700-e09d-11eb-8076-7fad81f98f70.png)

## Selenium wrapper to make your life easy

![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python)
![selemium](https://img.shields.io/badge/Selenium-e5dfde?style=for-the-badge&logo=selenium)
![s-tool](https://img.shields.io/badge/S-Tool-3776AB?style=for-the-badge)
![Python-World](https://img.shields.io/badge/Python-World-FFD43B?style=for-the-badge&logo=python&logoColor=white)

## Table of Contents

- [Key Features](#key-features)
- [How To Use](#how-to-use)
- [Examples](#examples)
- [Todo](#todo)
- [License](#license)

## Key Features

- WebDriver
  - Manage multiple web drivers such as chrome,chromium,firefox.
- Different Utilities
  - Retrieve elements with 5 different attributes.
  - Perform clicks on element.
  - Take a full page and element screenshot.
  - Hide and show elements.
  - Information filling on different form elements such as text,radio,checkbox.
  - Retrieves current cookies from the browser.
  - Injecting new cookies into browser.
  - Retrieve url and web page source.
  - Add or modify existing cookies.
  - Retrieve current user agent.
  - Check Existence of an element on the page.
- Element Parser
  - table Information.
  - Retrieve dropdown options in the dictionary.

## How To Use

### Install using PYPI

```bash
pip install s-tool
```

### Setup for development

To clone and run this application, you'll need [Git](https://git-scm.com) and
[Poetry](https://python-poetry.org/) and [python Version ^3.8](http://python.org/)

```bash
# Clone this repository
git clone https://github.com/Python-World/s-tool.git

# Go into the repository
cd s-tool

# Install dependencies
poetry config virtualenvs.in-project true
poetry install

# Start Poetry shell
poetry shell
```

Note: If you're doing development setup, [see this guide](CONTRIBUTING)

## Examples

### Example 1

```python
"""Example code with class"""

from s_tool.driver import SeleniumDriver


class SBot(SeleniumDriver):
   """Example Bot using s-tool"""

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)

   def run(self):
       self.get("https://google.com")
       sessionid = self.session()
       url = self.url()
       cookies = self.cookies()

       # print sessionid,url,cookies
       print(f"\n url     :   {url} \n session :   {sessionid}\n cookies :   {cookies}\n")


bot = SBot("firefox", headless=True)  # change headless=False to run with gui mode
bot.run()
bot.close()

```

### Example 2

```python
"""Example code with context manager"""

from s_tool.driver import SeleniumDriver as SBot

with SBot("firefox", headless=True) as obj:
   obj.get("https://google.com")
   sessionid = obj.session()
   url = obj.url()
   cookies = obj.cookies()

   # print sessionid,url,cookies
   print(f"\n url     :   {url} \n session :   {sessionid}\n cookies :   {cookies}\n")

```

## Todo

- Web driver utilities
  - Scrolling element and page.
  - Handling popup and alert boxes.
  - Switching windows,frames,tabs,iframes.
  - logger.
- Element Parser
  - list
  - radio and checkboxes

Note: If you have any idea to improve or optimized in better way
[create issue](https://github.com/Python-World/s-tool/issues/new) for discussion.

## License

[MIT](LICENSE)
