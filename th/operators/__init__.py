from typing import Any

from ._operator import Operator

__all__ = ("Operator", "AttrAccessor", "ItemAccessor",)


class AttrAccessor(Operator):
    def __call__(self, target: Any) -> Any:
        return getattr(target, self._operand)

    def __str__(self) -> str:
        return f".{self._operand}"


class ItemAccessor(Operator):
    def __call__(self, target: Any) -> Any:
        return target[self._operand]

    def __str__(self) -> str:
        return f"[{self._operand!r}]"
