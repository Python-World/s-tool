"""Example code with class"""

from s_tool.driver import SeleniumDriver


class SBot(SeleniumDriver):
    """Example Bot using s-tool"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        """Code to visit url and fetch cookies and basic info"""
        self.get("https://google.com")
        sessionid = self.session()
        url = self.url()
        cookies = self.cookies()

        # print sessionid,url,cookies
        print(f"\nurl     :   {url} \nsession :   {sessionid}\ncookies :   {cookies}\n")


bot = SBot("firefox", headless=True)  # change headless=False to run with gui mode
bot.run()
bot.close()
