from __future__ import annotations

from typing import Any, Callable, Dict, List, TYPE_CHECKING

from apix.attribute import *
from apix.cursor_type import *
from apix.document import *
from apix.filter_type import *
from apix.gql import *
from apix.order_type import *
from apix.select_type import *
from apix.update_type import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.select import *


__all__ = [
    'ApixModel',
]


class ApixModel(type):
    Id: ApixIdAttribute

    def __new__(
            mcs,
            name: str,
            attributes: List[ApixAttribute] | Callable[[], List[ApixAttribute]],
            *,
            gql_output_type_description: str = None,
            gql_output_field_description: str = None,
            gql_input_type_description: str = None,
            gql_input_field_description: str = None,
            gql_update_type_description: str = None,
            gql_filter_type_description: str = None,
            gql_order_type_description: str = None,
    ):

        if not is_snake_case(name):
            raise ValueError(f"Name '{name}' must be snake case.")

        return super().__new__(mcs, mcs.__name__, (ApixDocument,), {})

    def __init__(
            cls,
            name: str,
            attributes: List[ApixAttribute] | Callable[[], List[ApixAttribute]],
            *,
            gql_output_type_description: str = None,
            gql_output_field_description: str = None,
            gql_input_type_description: str = None,
            gql_input_field_description: str = None,
            gql_update_type_description: str = None,
            gql_filter_type_description: str = None,
            gql_order_type_description: str = None,
    ):

        super().__init__(cls.__name__, (ApixDocument,), {})

        cls.name = name
        cls._attributes = attributes
        cls.gql_output_type_description = gql_output_type_description
        cls.gql_output_field_description = gql_output_field_description
        cls.gql_input_type_description = gql_input_type_description
        cls.gql_input_field_description = gql_input_field_description
        cls.gql_update_type_description = gql_update_type_description
        cls.gql_filter_type_description = gql_filter_type_description
        cls.gql_order_type_description = gql_order_type_description

        cls.Filter = ApixFilterType(cls)
        cls.Update = ApixUpdateType(cls)
        cls.Order = ApixOrderType(cls)
        cls.Select = ApixSelectType(cls)
        cls.Cursor = ApixCursorType(cls)
        cls.AsyncCursor = ApixAsyncCursorType(cls)

    def __repr__(cls) -> str:
        return f'<{cls.__class__.__name__}:{cls.class_name}>'

    def __getattr__(
            cls,
            key: str
    ):

        if key in cls.attributes_by_class_name:
            for attribute in cls.attributes:
                setattr(cls, attribute.class_name, attribute)

        return super().__getattribute__(key)

    @cached_property
    def projection(cls) -> ApixSelectType:
        return ApixSelectType(cls)

    @cached_property
    def class_name(cls) -> str:
        return gql_snake_to_camel(cls.name, True)

    @cached_property
    def attributes(cls) -> List[ApixAttribute]:

        if is_lambda_function(cls._attributes):
            cls._attributes = cls._attributes()

        cls._attributes.insert(0, ApixIdAttribute('id', gql_input_included=False, gql_update_included=False))

        for attribute in cls._attributes:
            attribute._model = cls

        return cls._attributes

    @cached_property
    def attributes_by_name(cls) -> Dict[str, ApixAttribute]:
        return {attribute.name: attribute for attribute in cls.attributes}

    @cached_property
    def attributes_by_class_name(cls) -> Dict[str, ApixAttribute]:
        return {attribute.class_name: attribute for attribute in cls.attributes}

    @cached_property
    def attributes_by_field_name(cls) -> Dict[str, ApixAttribute]:
        return {attribute.field_name: attribute for attribute in cls.attributes}

    def get_attribute_by_name(cls, name: str) -> ApixAttribute | None:

        if name == 'id':
            name = '_id'

        return cls.attributes_by_name.get(name)

    def get_attribute_by_class_name(cls, name: str) -> ApixAttribute | None:
        return cls.attributes_by_class_name.get(name)

    def get_attribute_by_field_name(cls, name: str) -> ApixAttribute | None:
        return cls.attributes_by_field_name.get(name)

    def from_value(cls, value: Any) -> ApixDocument:

        if isinstance(value, cls):
            return value # noqa
        elif isinstance(value, dict):
            return cls(**value)
        else:
            raise Exception('Invalid value')

    def to_input(cls, value: ApixDocument) -> Any:

        input = {}

        for key, val in value.__dict__.items():
            attribute = cls.get_attribute_by_name(key)
            input[attribute.name] = attribute.to_input(val)

        return input

    def create_select_from_gql_resolve_info(cls, gql_resolve_info: GraphQLResolveInfo) -> ApixSelect:

        field_node = gql_resolve_info.field_nodes[0]
        attributes = []

        for selection_node in field_node.selection_set.selections:
            if isinstance(selection_node, FieldNode):
                attribute = cls.attributes_by_field_name.get(selection_node.name.value)
                attributes += attribute.get_attributes_from_field_node(selection_node)

        return cls.Select(*attributes)

    @cached_property
    def gql_output_type(cls) -> GraphQLObjectType:

        return GraphQLObjectType(
            name=cls.class_name,
            fields=lambda: {attribute.field_name: attribute.gql_output_field for attribute in cls.attributes if attribute.gql_output_included},
            description=cls.gql_output_type_description,
        )

    @cached_property
    def gql_input_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.class_name}Input',
            fields={attribute.field_name: attribute.gql_input_field for attribute in cls.attributes if attribute.gql_input_included},
            description=cls.gql_input_type_description,
            out_type=cls.gql_input_out_type,
        )

    def gql_input_out_type(cls, value: Dict) -> ApixModel:
        return cls(**value)
