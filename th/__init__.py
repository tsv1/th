from typing import Any, Callable, Generator, List, Tuple, Union

from ._nil import Nil

__version__ = "0.0.1"
__all__ = ("get", "_")


PathItem = Tuple[str, Callable[[Any], Any]]


class PathHolder:
    def __init__(self, name: str = "PathHolder()") -> None:
        self.__name = name
        self.__path: List[PathItem] = []

    def __iter__(self) -> Generator[PathItem, None, None]:
        path = self.__name
        for part, op in self.__path:
            path += part
            yield path, op

    def __getattr__(self, name: str) -> "PathHolder":
        self.__path += [(f".{name}", lambda target: getattr(target, name))]
        return self

    def __getitem__(self, key: Any) -> "PathHolder":
        self.__path += [(f"[{key!r}]", lambda target: target[key])]
        return self

    def __repr__(self) -> str:
        return self.__name + "".join(r for r, _ in self.__path)


class PathHolderProxy:
    def __init__(self, factory: Callable[[], PathHolder]) -> None:
        self.__factory = factory

    def __getattr__(self, name: str) -> PathHolder:
        return self.__factory().__getattr__(name)

    def __getitem__(self, key: Any) -> PathHolder:
        return self.__factory().__getitem__(key)


def get(obj: Any, part: PathHolder, default: Union[Any, Nil] = Nil) -> Any:
    ptr = obj
    for part, op in part:  # type: ignore
        try:
            ptr = op(ptr)
        except (KeyError, IndexError, TypeError, AttributeError) as e:
            if default is not Nil:
                return default
            raise e
    return ptr


_ = PathHolderProxy(lambda: PathHolder("_"))
