from typing import Any, Callable, Optional, Type

__all__ = ("get_indent", "get_carets",  "get_type_name",)


def get_indent(exc: Type[Exception], path: Optional[str] = None) -> str:
    """
    Compute the indentation for error messages based on the exception type and path.

    :param exc: The exception class.
    :param path: The string representation of the path traversed so far.
    :return: A string of spaces for indentation.
    """
    prefix = f"{exc.__module__}.{exc.__name__}: "
    if path is None:
        return " " * len(prefix)
    return " " * (len(prefix) + len(path) + 1)


def get_carets(obj: Any, *, repr: Callable[[Any], str] = repr) -> str:
    """
    Generate a string of carets (^) matching the length of the object's string representation.

    :param obj: The object to represent.
    :param repr: A function that returns the string representation of the object.
    :return: A string of carets.
    """
    representation = repr(obj)
    return "^" * len(representation)


def get_type_name(obj: Any) -> str:
    """
    Get the type name of an object.

    :param obj: The object whose type name is desired.
    :return: The name of the object's type.
    """
    return type(obj).__name__
