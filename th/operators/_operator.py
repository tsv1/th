from abc import ABC, abstractmethod
from typing import Any

__all__ = ("Operator",)


class Operator(ABC):
    """
    Defines an abstract base class for all operators.

    This class provides an interface for operators that manipulate or access
    elements from a given target using a stored operand. It requires subclasses
    to implement the `__call__` method.
    """

    def __init__(self, operand: Any) -> None:
        """
        Initialize the Operator with an operand.

        :param operand: The operand to be used in the operator's operation.
        """
        self._operand = operand

    @property
    def operand(self) -> Any:
        """
        Return the operand associated with this operator.

        :return: The operand used by this operator.
        """
        return self._operand

    @abstractmethod
    def __call__(self, target: Any) -> Any:
        """
        Perform the operation on the target using the stored operand.

        :param target: The target on which the operator is applied.
        :return: The result of applying the operator to the target.
        :raises NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError()

    def __eq__(self, other: Any) -> bool:
        """
        Compare two Operator instances for equality.

        :param other: The other object to compare.
        :return: True if both instances are of the same class and have the same attributes.
        """
        return isinstance(other, self.__class__) and (self.__dict__ == other.__dict__)

    def __repr__(self) -> str:
        """
        Return a formal string representation of the Operator instance.

        :return: A string that includes the class name and operand.
        """
        return f"{self.__class__.__name__}({self._operand!r})"
