from s_tool.utils import get_element


def select_options(element, swap=None, text_exclude=[]):
    """Return dropdown option in key value pair

    Args:
        element      : An select element
        text_exclude : list of values to exclude from result

    Returns:
        return dict of values and text of select element,
        return empty dict() if element is not valid or not exists
    """
    option_dict = dict()
    if element and hasattr(element, "tag_name") and element.tag_name == "select":
        options = get_element(element, "tag_name", "option", many=True)
        for option in options:
            func = option.get_attribute
            text, value = func("text"), func("value")
            if text not in text_exclude:
                if swap:
                    text, value = value, text
                option_dict[value] = text

    return option_dict
