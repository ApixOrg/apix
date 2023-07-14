from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from apix.filter import *
from apix.gql import *
from apix.operator import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.model import *


__all__ = [
    'ApixFilterType',
]


class ApixFilterType(type):

    def __new__(mcs, model: ApixModel):
        return super().__new__(mcs, ApixFilter.__name__, (ApixFilter,), {})

    def __init__(cls, model: ApixModel):

        super().__init__(ApixFilter.__name__, (ApixFilter,), {})
        cls.model = model

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.model.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.model.class_name}Filter',
            fields={
                'operator': ApixLogicalOperatorInputField,
                **{attribute.field_name: attribute.gql_comparison_field for attribute in cls.model.attributes if attribute.gql_filter_included}
             },
            description=cls.model.gql_filter_type_description,
            out_type=cls.gql_input_out_type,
        )

    def gql_input_out_type(cls, value: Dict) -> ApixFilter:

        operator = value.pop('operator')

        comparisons = []
        for val in value.values():
            comparisons += val

        return cls.model.Filter(*comparisons, operator=operator)
