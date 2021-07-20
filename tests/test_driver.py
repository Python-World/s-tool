from s_tool.driver import SeleniumDriver

from . import TEST_URL


def test_cookies():
    with SeleniumDriver("firefox", headless=True) as obj:
        obj.get("http://google.com")

        # Validate cookies type
        assert type(obj.cookies()) is dict

        # Drop all cookies
        obj.set_cookies(drop_all=True)
        assert obj.cookies() == {}

        # Set new cookies

        obj.set_cookies(name="s-tool", version="1.0")
        cookies = obj.cookies()
        assert cookies.get("name") == "s-tool"

        # Drop cookie by name
        obj.set_cookies(drop_keys={"version"})
        cookies = obj.cookies()
        assert cookies.get("version", 1) == 1
