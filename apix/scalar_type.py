from __future__ import annotations

from typing import Any, Callable, Dict, Tuple, Type, TYPE_CHECKING

from bson import ObjectId
from bson.errors import InvalidId


if TYPE_CHECKING:
    from apix.gql import *


__all__ = [
    'ApixScalarType',
]


def _raise_value_error(
        name: str,
        value: Any,
) -> None:

    raise ValueError(f'The input value cannot be converted to {name}: {value}')


class ApixScalarType(type):

    def __new__(
            mcs,
            name: str,
            bases: Tuple,
            attrs: Dict,
            scalar_type: Type,
            gql_scalar_type: GraphQLScalarType,
            call: Callable = None,
    ):

        return super().__new__(mcs, name, bases, attrs)

    def __init__(
            cls,
            name: str,
            bases: Tuple,
            attrs: Dict,
            scalar_type: Type,
            gql_scalar_type: GraphQLScalarType,
            call: Callable = None,
    ):

        super().__init__(name, bases, attrs)

        if call is None:
            call = scalar_type

        cls.scalar_type = scalar_type
        cls.gql_scalar_type = gql_scalar_type
        cls.call = call

    def __call__(cls, value: Any) -> ObjectId:
        try:
            return cls.call(value)
        except (ValueError, TypeError, InvalidId):
            raise ValueError(f'The input value cannot be converted to {cls.__name__}: {value}')

    def __instancecheck__(cls, value: Any) -> bool:
        return isinstance(value, cls.scalar_type)
