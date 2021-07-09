"""Example code with context manager"""

from s_tool.driver import SeleniumDriver as SBot

with SBot("firefox", headless=True) as self:
    self.get("https://google.com")
    sessionid = self.session()
    url = self.url()
    cookies = self.cookies()

    # print sessionid,url,cookies
    print(f"\nurl     :   {url} \nsession :   {sessionid}\ncookies :   {cookies}\n")
