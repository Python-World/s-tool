from s_tool.driver import SeleniumDriver
from s_tool.parser import get_table, select_options

from . import TEST_URL


def test_select():
    """Test dropdown related operations"""
    with SeleniumDriver("firefox", headless=True) as obj:

        obj.get(TEST_URL)

        # Test dropdown options with element id
        options_dicts = select_options(obj.element("sel1"))
        actual_result = {"1": "1", "2": "2", "3": "3", "4": "4"}
        assert options_dicts == actual_result

        # Test for invalid element
        options_dicts = select_options(obj.element("select_id", "id"))
        assert options_dicts == {}

        # Test for disabled dropdown
        options_dicts = select_options(obj.element('//select[@disabled=""]', "xpath"))
        assert options_dicts == {
            "default": "default",
            "1": "One",
            "2": "Two",
            "3": "Three",
        }

        # Test for swaping keys and values\
        elem = obj.element('//select[@disabled=""]', "xpath")
        options_dicts = select_options(elem, swap=True)
        assert options_dicts == {
            "default": "default",
            "One": "1",
            "Two": "2",
            "Three": "3",
        }


def test_table():
    """Test table rows"""
    with SeleniumDriver("firefox", headless=True) as obj:
        obj.get(TEST_URL)
        table = obj.element('//table[@class="table"]', "xpath")
        table_data = get_table(table)
        assert len(table_data) == 4
