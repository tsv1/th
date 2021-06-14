from abc import ABC, abstractmethod
from typing import Any

__all__ = ("Operator",)


class Operator(ABC):
    def __init__(self, operand: Any) -> None:
        self._operand = operand

    @property
    def operand(self) -> Any:
        return self._operand

    @abstractmethod
    def __call__(self, target: Any) -> Any:
        raise NotImplementedError()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and (self.__dict__ == other.__dict__)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._operand!r})"
