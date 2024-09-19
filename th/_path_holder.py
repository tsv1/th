from copy import deepcopy
from typing import Any, Dict, Generator, List, Optional

from niltype import Nil, Nilable

from .operators import AttrAccessor, ItemAccessor, Operator

__all__ = ("PathHolder",)


class PathHolder:
    """
    Holds a sequence of operations (path) to access attributes or items of an object.

    This class enables constructing and holding a series of operators, such as attribute
    accessors and item accessors, to represent a path that can be applied to an object
    in sequence.
    """

    def __init__(self, name: str = "PathHolder()", path: Nilable[List[Operator]] = Nil) -> None:
        """
        Initialize the PathHolder with a name and an optional list of operators.

        :param name: The name of the PathHolder, default is "PathHolder()".
        :param path: An optional list of operators representing the path, default is Nil.
        """
        self.__name = self.__name__ = name
        self.__path: List[Operator] = path if (path is not Nil) else []

    def __iter__(self) -> Generator[Operator, None, None]:
        """
        Yield each operator in the path.

        :return: A generator that yields operators in the path.
        """
        for operator in self.__path:
            yield operator

    def __getattr__(self, name: str) -> "PathHolder":
        """
        Add an attribute accessor to the path and return the updated PathHolder.

        :param name: The attribute name to be accessed.
        :return: A new PathHolder with the attribute accessor added to the path.
        """
        self.__path.append(AttrAccessor(name))
        return self

    def __getitem__(self, key: Any) -> "PathHolder":
        """
        Add an item accessor to the path and return the updated PathHolder.

        :param key: The key or index to be accessed.
        :return: A new PathHolder with the item accessor added to the path.
        """
        self.__path.append(ItemAccessor(key))
        return self

    def __repr__(self) -> str:
        """
        Return a formal string representation of the PathHolder.

        :return: A string representation of the PathHolder and its path.
        """
        return self.__name + "".join(str(x) for x in self.__path)

    def __eq__(self, other: Any) -> bool:
        """
        Compare two PathHolder instances for equality.

        :param other: The other object to compare.
        :return: True if both instances are of the same class and have the same attributes.
        """
        return isinstance(self, other.__class__) and (self.__dict__ == other.__dict__)

    def __copy__(self) -> "PathHolder":
        """
        Create a shallow copy of the PathHolder.

        :return: A new shallow-copied PathHolder.
        """
        return self.__class__(self.__name, self.__path)

    def __deepcopy__(self, memo: Optional[Dict[Any, Any]] = None) -> "PathHolder":
        """
        Create a deep copy of the PathHolder.

        :param memo: A dictionary used for memoization during deep copy, default is None.
        :return: A new deep-copied PathHolder.
        """
        return self.__class__(self.__name, [deepcopy(x, memo) for x in self.__path])

    def __len__(self) -> int:
        """
        Return the number of operators in the path.

        :return: The length of the path.
        """
        return len(self.__path)
