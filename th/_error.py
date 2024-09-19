__all__ = ("Error",)


class Error(Exception):
    """
    Represents a custom error with support for suppressed exceptions.

    This class extends the base `Exception` class and allows for an additional
    suppressed exception to be passed, which can be useful for wrapping and 
    re-raising exceptions while retaining the original error.
    """

    def __init__(self, message: str, suppressed: Exception):
        """
        Initialize the Error instance with a message and a suppressed exception.

        :param message: The error message describing the exception.
        :param suppressed: The original exception that is being suppressed.
        """
        self.message = message
        self.suppressed = suppressed

    def __str__(self) -> str:
        """
        Return the error message as a string.

        :return: The error message.
        """
        return self.message

    def __repr__(self) -> str:
        """
        Return a formal string representation of the Error instance.

        :return: A string that includes the module, class name, and message.
        """
        return f"{self.__class__.__module__}.{self.__class__.__name__}: {self.message}"
