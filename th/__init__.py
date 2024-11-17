from pprint import pformat
from typing import Any, Union

from niltype import Nil, NilType

from ._error import Error
from ._path_holder import PathHolder
from ._path_holder_proxy import PathHolderProxy
from ._utils import get_carets, get_indent, get_type_name
from ._version import version
from .operators import ItemAccessor

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
    is_prev_slice = False

    for operator in path:
        try:
            if is_prev_slice:
                ptr = [operator(item) for item in ptr]
            else:
                ptr = operator(ptr)
        except _AttributeError as suppressed:
            if default is not Nil:
                return default
            indent = get_indent(AttributeError, prev)
            carets = get_carets(operator.operand, repr=str)
            message = f"{path}\n{indent}{carets} does not exist"
            if verbose:
                message += f"\nwhere _ is {type(obj)}:\n{pformat(obj)}"
            raise AttributeError(message, suppressed) from None

        except _IndexError as suppressed:
            if default is not Nil:
                return default
            indent = get_indent(IndexError, prev)
            carets = get_carets(operator.operand)
            message = f"{path}\n{indent}{carets} out of range"
            if verbose:
                message += f"\nwhere _ is {type(obj)}:\n{pformat(obj)}"
            raise IndexError(message, suppressed) from None

        except _KeyError as suppressed:
            if default is not Nil:
                return default
            indent = get_indent(KeyError, prev)
            carets = get_carets(operator.operand)
            message = f"{path}\n{indent}{carets} does not exist"
            if verbose:
                message += f"\nwhere _ is {type(obj)}:\n{pformat(obj)}"
            raise KeyError(message, suppressed) from None

        except _TypeError as suppressed:
            if default is not Nil:
                return default
            if "object is not subscriptable" in str(suppressed):
                indent = get_indent(TypeError)
                carets = get_carets(prev, repr=str)
                type_name = get_type_name(ptr)
                message = f"{path}\n{indent}{carets} inappropriate type ({type_name})"
            else:
                indent = get_indent(TypeError, prev)
                carets = get_carets(operator.operand)
                type_name = get_type_name(operator.operand)
                message = f"{path}\n{indent}{carets} inappropriate type ({type_name})"
            if verbose:
                message += f"\nwhere _ is {type(obj)}:\n{pformat(obj)}"
            raise TypeError(message, suppressed) from None
        prev += str(operator)
        is_prev_slice = isinstance(operator, ItemAccessor) and isinstance(operator.operand, slice)
    return ptr


_ = hold = PathHolderProxy(lambda: PathHolder("_"))
