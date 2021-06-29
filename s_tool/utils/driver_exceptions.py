class SToolException(Exception):
    """
    Base Class for selenium tools Exceptions
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
