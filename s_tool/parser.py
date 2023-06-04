"""
Parser utilities using lxml
"""
from lxml.html import fromstring


class LxmlParser:
    """
    parse using response using lxml
    """

    def dropdown(self, html_string, text_exclude=None):
        """
        Parse a dropdown from an HTML string and return the options as a
        list of tuples containing key-value pairs.

        Args:
            html_string: str
                - The HTML string containing the dropdown element.
            text_exclude:list, optional
                - A list of values to exclude from the result.
                - Defaults to None.

        Returns:
            result: list
                - A list of tuples containing key-value pairs of the dropdown options.
        """
        if text_exclude is None:
            text_exclude = []

        tree = fromstring(html_string)

        options = tree.findall(".//option")
        result = []

        for option in options:
            text = option.text.strip()
            value = option.get("value", "").strip()

            if text and text not in text_exclude:
                result.append((text, value))

        return result

    def table(self, html_string):
        """
        Write your own custom parser class
        """
        raise NotImplementedError("table parser is not defined , Write your own custom parser")
