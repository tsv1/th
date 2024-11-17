from typing import Any

from ._operator import Operator

__all__ = ("Operator", "AttrAccessor", "ItemAccessor",)


class AttrAccessor(Operator):
    """
    Accesses an attribute of a target object using the stored operand.

    This operator retrieves an attribute from a target object, where the operand
    represents the attribute's name.
    """

    def __call__(self, target: Any) -> Any:
        """
        Retrieve the attribute from the target using the operand.

        :param target: The target object from which the attribute will be retrieved.
        :return: The value of the attribute.
        :raises AttributeError: If the attribute does not exist.
        """
        return getattr(target, self._operand)

    def __str__(self) -> str:
        """
        Return a string representation of the attribute access operation.

        :return: A string representing the attribute access, e.g., '.attribute'.
        """
        return f".{self._operand}"


class ItemAccessor(Operator):
    """
    Accesses an item from a target object using the stored operand.

    This operator retrieves an item from a target (such as a list or dictionary),
    where the operand represents the key or index.
    """

    def __call__(self, target: Any) -> Any:
        """
        Retrieve the item from the target using the operand.

        :param target: The target object from which the item will be retrieved.
        :return: The value of the item.
        :raises KeyError: If the key does not exist in the target.
        :raises IndexError: If the index is out of range.
        """
        return target[self._operand]

    def __str__(self) -> str:
        """
        Return a string representation of the item access operation.

        :return: A string representing the item access, e.g., '[key]'.
        """
        if isinstance(self._operand, slice):
            start = self._operand.start if self._operand.start is not None else ""
            stop = self._operand.stop if self._operand.stop is not None else ""
            step = self._operand.step if self._operand.step is not None else ""
            return f"[{start}:{stop}:{step}]"
        return f"[{self._operand!r}]"
