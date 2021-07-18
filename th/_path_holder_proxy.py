from copy import deepcopy
from typing import Any, Callable, Dict, Generator, Optional

from ._path_holder import PathHolder
from .operators import Operator

__all__ = ("PathHolderProxy",)


class PathHolderProxy:
    def __init__(self, factory: Callable[[], PathHolder]) -> None:
        self.__factory = factory

    def __iter__(self) -> Generator[Operator, None, None]:
        yield from ()

    def __getattr__(self, name: str) -> PathHolder:
        return self.__factory().__getattr__(name)

    def __getitem__(self, key: Any) -> PathHolder:
        return self.__factory().__getitem__(key)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__factory!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(self, other.__class__) and (self.__dict__ == other.__dict__)

    def __copy__(self) -> "PathHolderProxy":
        return self.__class__(self.__factory)

    def __deepcopy__(self, memo: Optional[Dict[Any, Any]] = None) -> "PathHolderProxy":
        return self.__class__(deepcopy(self.__factory, memo))

    def __len__(self) -> int:
        return 0
