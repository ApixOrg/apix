from __future__ import annotations

from typing import Dict, Tuple, TYPE_CHECKING

from apix.direction import *
from apix.gql import *
from apix.operator import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.attribute import *


__all__ = [
    'ApixDirectionType'
]


class ApixDirectionType(type):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, ApixDirection.__name__, (ApixDirection,), {})

    def __init__(cls, attribute: ApixAttribute):

        super().__init__(ApixDirection.__name__, (ApixDirection,), {})
        cls.name = 'direction'
        cls.attribute = attribute

    def __repr__(self) -> str:
        return f'<{self.__name__}:{self.attribute.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.attribute.class_path_name}DirectionItem',
            fields={
                'position': GraphQLInputField(GraphQLNonNull(GraphQLInt)),
                'operator': ApixDirectionOperatorInputField,
            },
            description=None,
            out_type=cls.gql_input_out_type,
        )

    def gql_input_out_type(cls, value: Dict) -> Tuple[int, ApixDirection]:
        return value.get('position'), cls(value.get('operator').value)

    @cached_property
    def gql_input_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_input_type,
            description=None,
        )
