"""Base class for field enums."""

from enum import Enum


class FieldEnum(str, Enum):
    """A ``str`` enum whose ``str()`` and ``format()`` return the raw value.

    Python 3.11+ changed ``str(StrEnum)`` to return ``ClassName.MEMBER``
    instead of the underlying value. This base class restores the intuitive
    behaviour so that enums can be used transparently in f-strings, query
    parameters, and anywhere a plain string is expected.
    """

    def __str__(self) -> str:
        return self.value

    def __format__(self, format_spec: str) -> str:
        return self.value.__format__(format_spec)
