from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from apix.gql import *
from apix.order import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.model import *


__all__ = [
    'ApixOrderType',
]


class ApixOrderType(type):

    def __new__(mcs, model: ApixModel):
        return super().__new__(mcs, ApixOrder.__name__, (ApixOrder,), {})

    def __init__(cls, model: ApixModel):

        super().__init__(ApixOrder.__name__, (ApixOrder,), {})
        cls.model = model

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.model.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.model.class_name}Order',
            fields={attribute.field_name: attribute.gql_direction_field for attribute in cls.model.attributes if attribute.gql_order_included},
            description=cls.model.gql_order_type_description,
            out_type=cls.gql_input_out_type,
        )

    def gql_input_out_type(cls, value: Dict) -> ApixOrder:

        directions = []

        for val in value.values():
            if val is not None:
                directions += val

        directions = [direction for _, direction in sorted(directions)]

        return cls.model.Order(*directions)
