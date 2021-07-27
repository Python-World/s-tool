from s_tool.exceptions import SToolException
from s_tool.utils import get_element


def select_options(element, swap=None, text_exclude=set()):
    """Return dropdown option in key value pair

    Args:
        element ([selenium.element]): An select element
        swap ([bool], optional): Value as key if True. Defaults to None.
        text_exclude (set, optional): to exclude from result. Defaults to set().

    Returns:
        [dict]: return dict of values and text of select element,
                return empty dict() if element is not valid or not exists
    """

    option_dict = dict()
    if element and hasattr(element, "tag_name") and element.tag_name == "select":
        options = get_element(element, "option", "tag_name", many=True)
        for option in options:
            func = option.get_attribute
            text, value = func("text"), func("value")
            if text not in text_exclude:
                if swap:
                    text, value = value, text
                option_dict[value] = text

    return option_dict


def get_table(table):
    """Return list of rows including header and footer of given table

    Args:
        A selenium table element

    Returns:
        return list of row list,
        return [] if table not valid
    """
    results = []
    if table and hasattr(table, "tag_name") and table.tag_name == "table":
        for rows in table.find_elements_by_tag_name("tr"):
            cell_data = []
            for cell in rows.find_elements_by_xpath("td | th"):
                colspan = cell.get_attribute("colspan")
                cell_text = cell.text
                if colspan:
                    cell_data.extend([cell_text] + [""] * (int(colspan) - 1))
                else:
                    cell_data.append(cell_text)
            results.append(cell_data)
    else:
        raise SToolException("INVALIDTABLE")
    return results
