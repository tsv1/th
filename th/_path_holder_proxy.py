from typing import Any, Callable

from ._path_holder import PathHolder

__all__ = ("PathHolderProxy",)


class PathHolderProxy:
    def __init__(self, factory: Callable[[], PathHolder]) -> None:
        self.__factory = factory

    def __getattr__(self, name: str) -> PathHolder:
        return self.__factory().__getattr__(name)

    def __getitem__(self, key: Any) -> PathHolder:
        return self.__factory().__getitem__(key)
