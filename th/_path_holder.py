from copy import deepcopy
from typing import Any, Dict, Generator, List, Optional

from niltype import Nil, Nilable

from .operators import AttrAccessor, ItemAccessor, Operator

__all__ = ("PathHolder",)


class PathHolder:
    def __init__(self, name: str = "PathHolder()", path: Nilable[List[Operator]] = Nil) -> None:
        self.__name = self.__name__ = name
        self.__path: List[Operator] = path if (path is not Nil) else []

    def __iter__(self) -> Generator[Operator, None, None]:
        for operator in self.__path:
            yield operator

    def __getattr__(self, name: str) -> "PathHolder":
        self.__path.append(AttrAccessor(name))
        return self

    def __getitem__(self, key: Any) -> "PathHolder":
        self.__path.append(ItemAccessor(key))
        return self

    def __repr__(self) -> str:
        return self.__name + "".join(str(x) for x in self.__path)

    def __eq__(self, other: Any) -> bool:
        return isinstance(self, other.__class__) and (self.__dict__ == other.__dict__)

    def __copy__(self) -> "PathHolder":
        return self.__class__(self.__name, self.__path)

    def __deepcopy__(self, memo: Optional[Dict[Any, Any]] = None) -> "PathHolder":
        return self.__class__(self.__name, [deepcopy(x, memo) for x in self.__path])
