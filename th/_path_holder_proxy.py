from copy import deepcopy
from typing import Any, Callable, Dict, Generator, Optional

from ._path_holder import PathHolder
from .operators import Operator

__all__ = ("PathHolderProxy",)


class PathHolderProxy:
    """
    A proxy class for lazy instantiation of PathHolder objects.

    This class defers the creation of a PathHolder instance until an operation is
    performed, such as attribute or item access.
    """

    def __init__(self, factory: Callable[[], PathHolder]) -> None:
        """
        Initialize the PathHolderProxy with a factory function for creating PathHolder.

        :param factory: A callable that returns a new PathHolder instance.
        """
        self.__factory = factory

    def __iter__(self) -> Generator[Operator, None, None]:
        """
        Yield nothing (no operators) as the proxy does not hold a path itself.

        :return: An empty generator.
        """
        yield from ()

    def __getattr__(self, name: str) -> PathHolder:
        """
        Retrieve an attribute from the proxied PathHolder instance.

        :param name: The attribute name to access.
        :return: The PathHolder instance with the attribute accessor added.
        """
        return self.__factory().__getattr__(name)

    def __getitem__(self, key: Any) -> PathHolder:
        """
        Retrieve an item from the proxied PathHolder instance.

        :param key: The key or index to access.
        :return: The PathHolder instance with the item accessor added.
        """
        return self.__factory().__getitem__(key)

    def __repr__(self) -> str:
        """
        Return a formal string representation of the PathHolderProxy.

        :return: A string representation of the PathHolderProxy and its factory.
        """
        return f"{self.__class__.__name__}({self.__factory!r})"

    def __eq__(self, other: Any) -> bool:
        """
        Compare two PathHolderProxy instances for equality.

        :param other: The other object to compare.
        :return: True if both instances are of the same class and have the same attributes.
        """
        return isinstance(self, other.__class__) and (self.__dict__ == other.__dict__)

    def __copy__(self) -> "PathHolderProxy":
        """
        Create a shallow copy of the PathHolderProxy.

        :return: A new shallow-copied PathHolderProxy.
        """
        return self.__class__(self.__factory)

    def __deepcopy__(self, memo: Optional[Dict[Any, Any]] = None) -> "PathHolderProxy":
        """
        Create a deep copy of the PathHolderProxy.

        :param memo: A dictionary used for memoization during deep copy, default is None.
        :return: A new deep-copied PathHolderProxy.
        """
        return self.__class__(deepcopy(self.__factory, memo))

    def __len__(self) -> int:
        """
        Return zero as the proxy itself does not hold any operators.

        :return: Zero (0).
        """
        return 0
