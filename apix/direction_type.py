from __future__ import annotations

from typing import Tuple, Type, TYPE_CHECKING

from apix.direction import *
from apix.gql import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.attribute import *


__all__ = [
    'ApixDirectionType',
    'ApixAscendingDirectionType',
    'ApixDescendingDirectionType',
]


class ApixDirectionType(type):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixDirection],
            attribute: ApixAttribute,
    ):

        return super().__new__(mcs, base.__name__, (base,), {})

    def __init__(
            cls,
            name: str,
            base: Type[ApixDirection],
            attribute: ApixAttribute,
    ):

        super().__init__(base.__name__, (base,), {})
        cls.name = name
        cls.base = base
        cls.attribute = attribute

    def __repr__(self) -> str:
        return f'<{self.__name__}:{self.attribute.class_name}>'

    @cached_property
    def field_name(cls) -> str:
        return gql_snake_to_camel(cls.name, False)

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return GraphQLInt

    def gql_input_out_type(cls, value: int) -> Tuple[int, ApixDirection]:
        return value, cls()

    @cached_property
    def gql_input_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_input_type,
            description=None,
        )


class ApixAscendingDirectionType(ApixDirectionType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'ascending', ApixAscendingDirection, attribute)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('ascending', ApixAscendingDirection, attribute)


class ApixDescendingDirectionType(ApixDirectionType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'descending', ApixDescendingDirection, attribute)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('descending', ApixDescendingDirection, attribute)
