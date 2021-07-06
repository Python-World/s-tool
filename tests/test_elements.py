from s_tool.driver import SeleniumDriver

from . import TEST_URL


def test_select_box():
    with SeleniumDriver("firefox", headless=True) as obj:
        obj.get(TEST_URL)

        select_value = "1"
        obj.fill({"select_dropdown": select_value})
        element = obj.element("name", "select_dropdown")
        for ele in element.find_elements_by_tag_name("option"):
            if ele.text == "One":
                assert ele.is_selected() is True
