__all__ = ("Error",)


class Error(Exception):
    def __init__(self, message: str, suppressed: Exception):
        self.message = message
        self.suppressed = suppressed

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__name__}: {self.message}"
