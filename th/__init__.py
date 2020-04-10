from pprint import pformat
from typing import Any, Union

from ._error import Error
from ._nil import Nil
from ._path_holder import PathHolder
from ._path_holder_proxy import PathHolderProxy

__version__ = "0.0.1"
__all__ = ("get", "_", "PathHolder", "PathHolderProxy",)

_AttributeError = AttributeError
_IndexError = IndexError
_KeyError = KeyError
_TypeError = TypeError


class AttributeError(Error, _AttributeError):
    pass


class IndexError(Error, _AttributeError):
    pass


class KeyError(Error, _KeyError):
    pass


class TypeError(Error, _TypeError):
    pass


def get(obj: Any, path: PathHolder, *,
        default: Union[Any, Nil] = Nil, verbose: bool = False) -> Any:
    ptr = obj
    prev = path.__name__
    for part, operator, operand in path:
        try:
            ptr = operator(ptr)
        except _AttributeError as suppressed:
            if default is not Nil:
                return default
            prefix = f"{AttributeError.__module__}.{AttributeError.__name__}: "
            message = "{path}\n{indent}{carets} does not exist".format(
                path=path,
                indent=" " * (len(prefix) + len(prev) + 1),
                carets="^" * len(str(operand)),
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
                carets="^" * len(repr(operand)),
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
                carets="^" * len(repr(operand)),
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
                    carets="^" * len(repr(operand)),
                    type=type(operand).__name__,
                )
            if verbose:
                message += "\nwhere _ is {type}:\n{val}".format(type=type(obj), val=pformat(obj))
            raise TypeError(message, suppressed) from None
        prev = part
    return ptr


_ = PathHolderProxy(lambda: PathHolder("_"))
