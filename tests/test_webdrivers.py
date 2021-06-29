from s_tool.driver import SeleniumDriver


def test_firefox_driver():
    """Test firefox driver with headless"""
    with SeleniumDriver("firefox", headless=True) as obj:
        assert "firefox" in obj.browser_list
