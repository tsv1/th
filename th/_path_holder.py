from typing import Any, Callable, Generator, List, Tuple

__all__ = ("PathHolder",)

PathItem = Tuple[str, Callable[[Any], Any], Any]


class PathHolder:
    def __init__(self, name: str = "PathHolder()") -> None:
        self.__name = self.__name__ = name
        self.__path: List[PathItem] = []

    def __iter__(self) -> Generator[PathItem, None, None]:
        path = self.__name
        for part, operator, operand in self.__path:
            path += part
            yield path, operator, operand

    def __getattr__(self, name: str) -> "PathHolder":
        self.__path += [(f".{name}", lambda target: getattr(target, name), name)]
        return self

    def __getitem__(self, key: Any) -> "PathHolder":
        self.__path += [(f"[{key!r}]", lambda target: target[key], key)]
        return self

    def __repr__(self) -> str:
        return self.__name + "".join(part for part, *_ in self.__path)
