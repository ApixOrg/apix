from __future__ import annotations

from datetime import datetime
from typing import Union

from bson import ObjectId

from apix.gql import *
from apix.scalar_type import *


__all__ = [
    'ApixScalar',
    'ApixId',
    'ApixString',
    'ApixInteger',
    'ApixFloat',
    'ApixBoolean',
    'ApixDateTime',
]


class ApixId(metaclass=ApixScalarType, scalar_type=ObjectId, gql_scalar_type=GraphQLID):
    pass


class ApixString(metaclass=ApixScalarType, scalar_type=str, gql_scalar_type=GraphQLString):
    pass


class ApixInteger(metaclass=ApixScalarType, scalar_type=int, gql_scalar_type=GraphQLInt):
    pass


class ApixFloat(metaclass=ApixScalarType, scalar_type=float, gql_scalar_type=GraphQLFloat):
    pass


class ApixBoolean(metaclass=ApixScalarType, scalar_type=bool, gql_scalar_type=GraphQLBoolean):
    pass


class ApixDateTime(metaclass=ApixScalarType, scalar_type=datetime, gql_scalar_type=GraphQLDateTime, call=lambda value: value if isinstance(value, datetime) else datetime.fromisoformat(value)): # noqa
    pass


ApixScalar = Union[ApixId, ApixString, ApixInteger, ApixFloat, ApixBoolean, ApixDateTime]
