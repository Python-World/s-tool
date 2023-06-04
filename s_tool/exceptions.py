
"""
Exception classes
"""


class InvalidWebDriverError(Exception):
    """Custom exception raised for an invalid WebDriver."""


class SToolException(Exception):
    """
    Base Class for selenium tools Exceptions
    """

    def __init__(self, message):
        """[summary]

        Args:
            message ([str]): Exception message
        """
        self.message = message

    def __str__(self):
        """Return Exception message

        Returns:
            [str]: Exception
        """
        return str(self.message)
