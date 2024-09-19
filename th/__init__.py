from pprint import pformat
from typing import Any, Union

from niltype import Nil, NilType

from ._error import Error
from ._path_holder import PathHolder
from ._path_holder_proxy import PathHolderProxy
from ._version import version

__version__ = version
__all__ = ("get", "_", "PathHolder", "PathHolderProxy",)

_AttributeError = AttributeError
_IndexError = IndexError
_KeyError = KeyError
_TypeError = TypeError


class AttributeError(Error, _AttributeError):
    """
    Represents an AttributeError wrapped in a custom Error class.
    """
    pass


class IndexError(Error, _AttributeError):
    """
    Represents an IndexError wrapped in a custom Error class.
    """
    pass


class KeyError(Error, _KeyError):
    """
    Represents a KeyError wrapped in a custom Error class.
    """
    pass


class TypeError(Error, _TypeError):
    """
    Represents a TypeError wrapped in a custom Error class.
    """
    pass


def get(obj: Any, path: PathHolder, *,
        default: Union[Any, NilType] = Nil, verbose: bool = False) -> Any:
    """
    Retrieve the value at a given path from the target object.

    This function attempts to traverse the given `path` on the `obj`. If any attribute,
    key, or index does not exist, and a `default` value is provided, the default value
    will be returned. If no default is provided, a custom error (AttributeError, IndexError,
    KeyError, or TypeError) is raised with additional path information.

    :param obj: The target object from which to retrieve the value.
    :param path: A PathHolder representing the series of accessors (attributes or items).
    :param default: The default value to return if the path is not valid. Default is `Nil`.
    :param verbose: If True, additional debug information will be included in the error message.
    :return: The value retrieved from the object at the specified path.
    :raises AttributeError: If an attribute in the path does not exist and no default is provided.
    :raises IndexError: If an index in the path is out of range and no default is provided.
    :raises KeyError: If a key in the path does not exist and no default is provided.
    :raises TypeError: If an operation in the path is inappropriate for the object type and
                       no default is provided.
    """
    ptr = obj
    prev = path.__name__
    for operator in path:
        try:
            ptr = operator(ptr)
        except _AttributeError as suppressed:
            if default is not Nil:
                return default
            prefix = f"{AttributeError.__module__}.{AttributeError.__name__}: "
            message = "{path}\n{indent}{carets} does not exist".format(
                path=path,
                indent=" " * (len(prefix) + len(prev) + 1),
                carets="^" * len(str(operator.operand)),
            )
            if verbose:
                message += "\nwhere _ is {type}:\n{val}".format(type=type(obj), val=pformat(obj))
            raise AttributeError(message, suppressed) from None
        except _IndexError as suppressed:
            if default is not Nil:
                return default
            prefix = f"{IndexError.__module__}.{IndexError.__name__}: "
            message = "{path}\n{indent}{carets} out of range".format(
                path=path,
                indent=" " * (len(prefix) + len(prev) + 1),
                carets="^" * len(repr(operator.operand)),
            )
            if verbose:
                message += "\nwhere _ is {type}:\n{val}".format(type=type(obj), val=pformat(obj))
            raise IndexError(message, suppressed) from None
        except _KeyError as suppressed:
            if default is not Nil:
                return default
            prefix = f"{KeyError.__module__}.{KeyError.__name__}: "
            message = "{path}\n{indent}{carets} does not exist".format(
                path=path,
                indent=" " * (len(prefix) + len(prev) + 1),
                carets="^" * len(repr(operator.operand)),
            )
            if verbose:
                message += "\nwhere _ is {type}:\n{val}".format(type=type(obj), val=pformat(obj))
            raise KeyError(message, suppressed) from None
        except _TypeError as suppressed:
            if default is not Nil:
                return default
            prefix = f"{TypeError.__module__}.{TypeError.__name__}: "
            if "object is not subscriptable" in str(suppressed):
                message = "{path}\n{indent}{carets} inappropriate type ({type})".format(
                    path=path,
                    indent=" " * len(prefix),
                    carets=len(prev) * '^',
                    type=type(ptr).__name__,
                )
            else:
                message = "{path}\n{indent}{carets} inappropriate type ({type})".format(
                    path=path,
                    indent=" " * (len(prefix) + len(prev) + 1),
                    carets="^" * len(repr(operator.operand)),
                    type=type(operator.operand).__name__,
                )
            if verbose:
                message += "\nwhere _ is {type}:\n{val}".format(type=type(obj), val=pformat(obj))
            raise TypeError(message, suppressed) from None
        prev += str(operator)
    return ptr


_ = hold = PathHolderProxy(lambda: PathHolder("_"))
