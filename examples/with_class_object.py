"""Example code with class"""

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
