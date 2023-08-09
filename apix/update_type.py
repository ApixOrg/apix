from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from apix.gql import *
from apix.update import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.model import *


__all__ = [
    'ApixUpdateType',
]


class ApixUpdateType(type):

    def __new__(mcs, model: ApixModel):
        return super().__new__(mcs, ApixUpdate.__name__, (ApixUpdate,), {})

    def __init__(cls, model: ApixModel):

        super().__init__(ApixUpdate.__name__, (ApixUpdate,), {})
        cls.model = model

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.model.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.model.class_name}Update',
            fields={attribute.field_name: attribute.gql_operation_field for attribute in cls.model.attributes if attribute.gql_update_included},
            description=cls.model.gql_update_type_description,
            out_type=cls.gql_input_out_type,
        )

    def gql_input_out_type(
            cls,
            value: Dict,
    ) -> ApixUpdate:

        operations = []

        for val in value.values():
            if val is not None:
                operations += val

        return cls.model.Update(*operations)
