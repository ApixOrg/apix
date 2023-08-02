from __future__ import annotations

from inspect import signature
from typing import Any, Callable, Dict, List, Tuple, Type, TYPE_CHECKING

from apix.comparison_type import *
from apix.direction_type import *
from apix.document import *
from apix.enumeration import *
from apix.gql import *
from apix.operation_type import *
from apix.utils import *
from apix.scalar import *


if TYPE_CHECKING:
    from apix.comparison import *
    from apix.direction import *
    from apix.model import *
    from apix.operation import *


__all__ = [
    'ApixAttribute',
    'ApixScalarAttribute',
    'ApixIdAttribute',
    'ApixStringAttribute',
    'ApixIntegerAttribute',
    'ApixFloatAttribute',
    'ApixBooleanAttribute',
    'ApixDateTimeAttribute',
    'ApixEnumerationAttribute',
    'ApixListAttribute',
    'ApixObjectAttribute',
    'ApixReferenceAttribute',
]


class ApixAttribute(type):

    reserved_names = [
        'is_null', 'equal', 'not_equal', 'less_than', 'less_than_equal', 'greater_than', 'greater_than_equal', 'in', 'not_in',
        'any_is_null', 'any_equal', 'any_not_equal', 'any_less_than', 'any_less_than_equal', 'any_greater_than', 'any_greater_than_equal', 'any_in', 'any_not_in',
        'set', 'unset', 'increment', 'multiply', 'min', 'max', 'pull', 'pop',
        'direction',
        'filter', 'update', 'order', 'select', 'cursor', 'async_cursor',
        'operator',
    ]

    def __new__(
            mcs,
            name: str,
            bases: Tuple,
            *,
            gql_output_included: bool = True,
            gql_output_nullable: bool = True,
            gql_output_field_description: str = None,
            gql_input_included: bool = True,
            gql_input_nullable: bool = True,
            gql_input_field_description: str = None,
            gql_update_included: bool = True,
            gql_filter_included: bool = True,
            gql_order_included: bool = True,
    ):

        if not isinstance(name, str):
            raise TypeError("The argument 'name' must be a string")
        elif not is_snake_case(name):
            raise ValueError("The argument 'name' must be snake case")
        elif name in mcs.reserved_names:
            raise ValueError("The argument 'name' must be a reserved name")

        if not isinstance(gql_output_included, bool):
            raise TypeError("The argument 'gql_output_included' must be a boolean")

        if not isinstance(gql_output_nullable, bool):
            raise TypeError("The argument 'gql_output_nullable' must be a boolean")

        if gql_output_field_description is not None:
            if not isinstance(gql_output_field_description, str):
                raise TypeError("The argument 'gql_output_field_description' must be a string")

        if not isinstance(gql_input_included, bool):
            raise TypeError("The argument 'gql_input_included' must be a boolean")

        if not isinstance(gql_input_nullable, bool):
            raise TypeError("The argument 'gql_input_nullable' must be a boolean")

        if gql_input_field_description is not None:
            if not isinstance(gql_input_field_description, str):
                raise TypeError("The argument 'gql_input_field_description' must be a string")

        if not isinstance(gql_update_included, bool):
            raise TypeError("The argument 'gql_update_included' must be a boolean")

        if not isinstance(gql_filter_included, bool):
            raise TypeError("The argument 'gql_filter_included' must be a boolean")

        if not isinstance(gql_order_included, bool):
            raise TypeError("The argument 'gql_order_included' must be a boolean")

        return super().__new__(mcs, gql_snake_to_camel(name, True), bases, {})

    def __init__(
            cls,
            name: str,
            bases: Tuple,
            *,
            gql_output_included: bool = True,
            gql_output_nullable: bool = True,
            gql_output_field_description: str = None,
            gql_input_included: bool = True,
            gql_input_nullable: bool = True,
            gql_input_field_description: str = None,
            gql_update_included: bool = True,
            gql_filter_included: bool = True,
            gql_order_included: bool = True,
    ):

        super().__init__(gql_snake_to_camel(name, True), bases, {})

        cls._name = name
        cls.bases = bases

        cls.gql_output_included = gql_output_included
        cls.gql_output_nullable = gql_output_nullable
        cls.gql_output_nullable = gql_output_nullable
        cls.gql_output_field_description = gql_output_field_description
        cls.gql_input_included = gql_input_included
        cls.gql_input_nullable = gql_input_nullable
        cls.gql_input_field_description = gql_input_field_description
        cls.gql_update_included = gql_update_included
        cls.gql_filter_included = gql_filter_included
        cls.gql_order_included = gql_order_included

        cls.IsNull = ApixIsNullComparisonType(cls)
        cls.Equal = ApixEqualComparisonType(cls)
        cls.NotEqual = ApixNotEqualComparisonType(cls)
        cls.LessThan = ApixLessThanComparisonType(cls)
        cls.LessThanEqual = ApixLessThanEqualComparisonType(cls)
        cls.GreaterThan = ApixGreaterThanComparisonType(cls)
        cls.GreaterThanEqual = ApixGreaterThanEqualComparisonType(cls)
        cls.In = ApixInComparisonType(cls)
        cls.NotIn = ApixNotInComparisonType(cls)

        cls.Set = ApixSetOperationType(cls)
        cls.Unset = ApixUnsetOperationType(cls)

        cls.Direction: Type[ApixDirection] = ApixDirectionType(cls) # noqa

        cls._model = None
        cls._parent = None
        cls._index = None

    def __repr__(cls) -> str:
        return f'<{cls.__class__.__name__}:{cls.__name__}>'

    def __getattr__(cls, key: str):

        if cls.get_attribute_by_class_name(key):
            for attribute in cls.attributes:
                setattr(cls, attribute.class_name, attribute)

        return super().__getattribute__(key)

    @cached_property
    def attribute(cls) -> ApixAttribute | None:
        raise NotImplementedError

    @cached_property
    def attributes(cls) -> List[ApixAttribute]:
        raise NotImplementedError

    @cached_property
    def kwargs(cls) -> Dict[str, Any]:
        raise NotImplementedError

    @cached_property
    def gql_input_type(cls) -> GraphQLScalarType | GraphQLEnumType | GraphQLInputObjectType:
        raise NotImplementedError

    @cached_property
    def gql_output_type(cls) -> GraphQLScalarType | GraphQLEnumType | GraphQLObjectType:
        raise NotImplementedError

    def from_value(cls, value: Any) -> ApixAttribute:
        raise NotImplementedError

    def to_input(cls, value: Any) -> Any:
        raise NotImplementedError

    def resolve_gql_output_field(
            cls,
            source: ApixDocument,
            _: GraphQLResolveInfo,
    ) -> Any:

        if hasattr(source, cls._name):
            return getattr(source, cls._name)

    def get_attributes_from_field_node(
            cls,
            field_node: FieldNode
    ) -> List[ApixAttribute]:

        attributes = []

        if field_node.selection_set:
            for selection_node in field_node.selection_set.selections:
                if isinstance(selection_node, FieldNode):
                    attribute = cls.attributes_by_field_name.get(selection_node.name.value)
                    attributes += attribute.get_attributes_from_field_node(selection_node)
        else:
            attributes += [cls]

        return attributes

    @cached_property
    def name(cls) -> str:
        return '_id' if cls._name == 'id' else cls._name

    @cached_property
    def class_name(cls) -> str:
        return gql_snake_to_camel(cls._name, True)

    @cached_property
    def field_name(cls) -> str:
        return gql_snake_to_camel(cls._name, False)

    @cached_property
    def path_name(cls) -> str:

        names = [attribute.name if attribute.index is None else f'{attribute.index}' for attribute in cls.path]
        return '.'.join(names)

    @cached_property
    def class_path_name(cls) -> str:

        names = []

        for attribute in cls.path:
            if attribute.index is not None:
                names.pop(-1)
            names.append(attribute.class_name)

        if cls.model:
            names.insert(0, cls.model.class_name)

        return ''.join(names)

    @cached_property
    def model(cls) -> ApixModel | None:
        return cls._model

    @cached_property
    def parent(cls) -> ApixListAttribute | ApixObjectAttribute | ApixReferenceAttribute | None:
        return cls._parent

    @cached_property
    def index(cls) -> int | None:
        return cls._index

    @cached_property
    def path(cls) -> List[ApixAttribute]:

        path = []
        attribute = cls

        while attribute:
            path.append(attribute)
            attribute = attribute.parent

        return list(reversed(path))

    @cached_property
    def lookup_attribute(cls) -> ApixReferenceAttribute | ApixListAttribute | None:

        for attribute in cls.path:
            if isinstance(attribute, ApixReferenceAttribute) or (isinstance(attribute, ApixListAttribute) and isinstance(attribute.attribute, ApixReferenceAttribute)):
                return attribute

    @cached_property
    def sub_attribute(cls) -> ApixAttribute | None:

        sub_attribute = None

        for attribute in cls.path:
            if sub_attribute:
                sub_attribute = sub_attribute.get_attribute_by_name(attribute.name)
            elif cls != attribute:
                if isinstance(attribute, ApixReferenceAttribute):
                    sub_attribute = attribute.reference
                elif isinstance(attribute, ApixListAttribute) and isinstance(attribute.attribute, ApixReferenceAttribute):
                    sub_attribute = attribute.attribute.reference

        return sub_attribute

    @cached_property
    def attributes_by_name(cls) -> Dict[str, ApixAttribute]:
        return {attribute.name: attribute for attribute in cls.attributes}

    @cached_property
    def attributes_by_class_name(cls) -> Dict[str, ApixAttribute]:
        return {attribute.class_name: attribute for attribute in cls.attributes}

    @cached_property
    def attributes_by_field_name(cls) -> Dict[str, ApixAttribute]:
        return {attribute.field_name: attribute for attribute in cls.attributes}

    def get_attribute_by_name(
            cls,
            name: str,
    ) -> ApixAttribute | None:

        if name == 'id':
            name = '_id'

        return cls.attributes_by_name.get(name)

    def get_attribute_by_class_name(
            cls,
            name: str,
    ) -> ApixAttribute | None:

        return cls.attributes_by_class_name.get(name)

    def get_attribute_by_field_name(
            cls,
            name: str,
    ) -> ApixAttribute | None:

        return cls.attributes_by_field_name.get(name)

    def copy(cls) -> ApixAttribute:
        return cls.__class__(**cls.kwargs)

    @cached_property
    def is_scalar_attribute(cls) -> bool:
        return isinstance(cls, ApixScalarAttribute)

    @cached_property
    def is_list_attribute(cls) -> bool:
        return isinstance(cls, ApixListAttribute)

    @cached_property
    def is_object_attribute(cls) -> bool:
        return isinstance(cls, ApixObjectAttribute)

    @cached_property
    def is_reference_attribute(cls) -> bool:
        return isinstance(cls, ApixReferenceAttribute)

    @cached_property
    def is_from_reference_attribute(cls) -> bool:
        return isinstance(cls.parent, ApixReferenceAttribute) or (isinstance(cls.parent, ApixListAttribute) and isinstance(cls.parent.attribute, ApixReferenceAttribute))

    @cached_property
    def comparison_types(cls) -> List[ApixComparisonType]:
        return [attr for attr in cls.__dict__.values() if isinstance(attr, ApixComparisonType)]

    @cached_property
    def comparison_types_by_field_name(cls) -> Dict[str, ApixComparisonType]:
        return {comparison_type.field_name: comparison_type for comparison_type in cls.comparison_types}

    @cached_property
    def operation_types(cls) -> List[ApixOperationType]:
        return [attr for attr in cls.__dict__.values() if isinstance(attr, ApixOperationType)]

    @cached_property
    def operation_types_by_field_name(cls) -> Dict[str, ApixOperationType]:
        return {operation_type.field_name: operation_type for operation_type in cls.operation_types}

    @cached_property
    def gql_wrapped_input_type(cls) -> GraphQLNonNull | GraphQLScalarType | GraphQLEnumType | GraphQLInputObjectType:

        if cls.gql_input_nullable:
            return cls.gql_input_type
        else:
            return GraphQLNonNull(cls.gql_input_type)

    @cached_property
    def gql_input_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_wrapped_input_type,
            description=cls.gql_input_field_description,
            out_name=cls.name,
        )

    @cached_property
    def gql_wrapped_output_type(cls) -> GraphQLNonNull | GraphQLScalarType | GraphQLEnumType | GraphQLObjectType:

        if cls.gql_output_nullable:
            return cls.gql_output_type
        else:
            return GraphQLNonNull(cls.gql_output_type)

    @cached_property
    def gql_output_field(cls) -> GraphQLField:

        return GraphQLField(
            type_=cls.gql_wrapped_output_type,
            description=cls.gql_output_field_description,
            resolve=cls.resolve_gql_output_field,
        )

    @cached_property
    def gql_comparison_type_fields(cls) -> Dict[str, GraphQLInputField]:

        fields = {}

        for comparison_type in cls.comparison_types:
            fields[comparison_type.field_name] = comparison_type.gql_input_field

        for attribute in cls.attributes:
            if not attribute.is_from_reference_attribute:
                fields[attribute.field_name] = attribute.gql_comparison_field

        if cls.attribute:
            fields[cls.attribute.field_name] = cls.gql_element_comparison_field

        return fields

    @cached_property
    def gql_comparison_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.class_path_name}Comparison',
            fields=cls.gql_comparison_type_fields,
            description=None,
            out_type=cls.gql_comparison_out_type,
        )

    def gql_comparison_out_type(
            cls,
            value: Dict,
    ) -> List[ApixComparison]:

        comparisons = []

        for key, val in value.items():
            if val is not None:

                if key in cls.comparison_types_by_field_name:
                    comparison_type = cls.comparison_types_by_field_name.get(key)
                    comparisons.append(comparison_type.from_value(val))

                elif key in cls.attributes_by_field_name:
                    comparisons += val

                else:
                    for element_comparison in val:
                        comparisons += element_comparison

        return comparisons

    @cached_property
    def gql_comparison_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_comparison_type,
            description=None,
        )

    @cached_property
    def gql_operation_type_fields(cls) -> Dict[str, GraphQLInputField]:

        fields = {}

        for operation_type in cls.operation_types:
            fields[operation_type.field_name] = operation_type.gql_input_field

        for attribute in cls.attributes:
            if not attribute.is_from_reference_attribute:
                fields[attribute.field_name] = attribute.gql_operation_field

        if cls.attribute:
            fields[cls.attribute.field_name] = cls.gql_element_operation_field

        return fields

    @cached_property
    def gql_operation_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.class_path_name}Operation',
            fields=cls.gql_operation_type_fields,
            description=None,
            out_type=cls.gql_operation_out_type,
        )

    def gql_operation_out_type(
            cls,
            value: Dict,
    ) -> List[ApixOperation]:

        operations = []

        for key, val in value.items():
            if val is not None:

                if key in cls.operation_types_by_field_name:
                    operation_type = cls.operation_types_by_field_name.get(key)
                    operations.append(operation_type.from_value(val))

                elif key in cls.attributes_by_field_name:
                    operations += val

                else:
                    for element_operation in val:
                        operations += element_operation

        return operations

    @cached_property
    def gql_operation_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_operation_type,
            description=None,
        )

    @cached_property
    def gql_direction_type_fields(cls) -> Dict[str, GraphQLInputField]:

        fields = {'direction': cls.Direction.gql_input_field} # noqa

        for attribute in cls.attributes:
            if not attribute.is_from_reference_attribute:
                fields[attribute.field_name] = attribute.gql_direction_field

        if cls.attribute:
            fields[cls.attribute.field_name] = cls.gql_element_direction_field

        return fields

    @cached_property
    def gql_direction_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.class_path_name}Direction',
            fields=cls.gql_direction_type_fields,
            description=None,
            out_type=cls.gql_direction_out_type,
        )

    def gql_direction_out_type(
            cls,
            value: Dict,
    ) -> List[Tuple[int, ApixDirection]]:

        directions = []

        for key, val in value.items():
            if val is not None:

                if key == 'direction':
                    directions.append(val)

                elif key in cls.attributes_by_field_name:
                    directions += val

                else:
                    for element_direction in val:
                        directions += element_direction

        return directions

    @cached_property
    def gql_direction_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_direction_type,
            description=None,
        )


class ApixScalarAttribute(ApixAttribute):

    def __new__(
            mcs,
            name: str,
            scalar_type: Type[ApixScalar],
            **kwargs,
    ):
        return super().__new__(mcs, name, (), **kwargs)

    def __init__(
            cls,
            name: str,
            scalar_type: Type[ApixScalar],
            **kwargs,
    ):

        super().__init__(name, (), **kwargs)
        cls.scalar_type = scalar_type
        cls._kwargs = kwargs

    def __call__(cls, value: Any) -> Any:
        return cls.scalar_type(value)

    @cached_property
    def attribute(cls) -> ApixAttribute | None:
        return None

    @cached_property
    def attributes(cls) -> List[ApixAttribute]:
        return []

    @cached_property
    def kwargs(cls) -> Dict[str, Any]:

        return {
            'name': cls._name,
            **cls._kwargs,
        }

    @cached_property
    def gql_input_type(cls) -> GraphQLScalarType:
        return cls.scalar_type.gql_scalar_type

    @cached_property
    def gql_output_type(cls) -> GraphQLScalarType:
        return cls.scalar_type.gql_scalar_type

    def from_value(cls, value: Any) -> ApixScalar:
        return cls(value)

    def to_input(cls, value: Any) -> Any:
        return value


class ApixIdAttribute(ApixScalarAttribute):

    def __new__(mcs, name: str, **kwargs):
        return super().__new__(mcs, name, ApixId, **kwargs)

    def __init__(cls, name: str, **kwargs):
        super().__init__(name, ApixId, **kwargs)


class ApixStringAttribute(ApixScalarAttribute):

    def __new__(mcs, name: str, **kwargs):
        return super().__new__(mcs, name, ApixString, **kwargs)

    def __init__(cls, name: str, **kwargs):
        super().__init__(name, ApixString, **kwargs)


class ApixIntegerAttribute(ApixScalarAttribute):

    def __new__(mcs, name: str, **kwargs):
        return super().__new__(mcs, name, ApixInteger, **kwargs)

    def __init__(cls, name: str, **kwargs):
        super().__init__(name, ApixInteger, **kwargs)

        cls.Increment = ApixIncrementOperationType(cls)
        cls.Multiply = ApixMultiplyOperationType(cls)
        cls.Min = ApixMinOperationType(cls)
        cls.Max = ApixMaxOperationType(cls)


class ApixFloatAttribute(ApixScalarAttribute):

    def __new__(mcs, name: str, **kwargs):
        return super().__new__(mcs, name, ApixFloat, **kwargs)

    def __init__(cls, name: str, **kwargs):
        super().__init__(name, ApixFloat, **kwargs)

        cls.Increment = ApixIncrementOperationType(cls)
        cls.Multiply = ApixMultiplyOperationType(cls)
        cls.Min = ApixMinOperationType(cls)
        cls.Max = ApixMaxOperationType(cls)


class ApixBooleanAttribute(ApixScalarAttribute):

    def __new__(mcs, name: str, **kwargs):
        return super().__new__(mcs, name, ApixBoolean, **kwargs)

    def __init__(cls, name: str, **kwargs):
        super().__init__(name, ApixBoolean, **kwargs)


class ApixDateTimeAttribute(ApixScalarAttribute):

    def __new__(
            mcs,
            name: str,
            **kwargs,
    ):
        return super().__new__(mcs, name, ApixDateTime, **kwargs)

    def __init__(
            cls,
            name: str,
            **kwargs,
    ):
        super().__init__(name, ApixDateTime, **kwargs)


class ApixEnumerationAttribute(ApixAttribute):

    def __new__(
            mcs,
            name: str,
            enumeration_values: List[ApixEnumerationValue],
            *,
            gql_enumeration_type_description: str = None,
            **kwargs,
    ):

        if not isinstance(enumeration_values, list):
            raise TypeError("The argument 'enumeration_values' must be a list")

        for enumeration_value in enumeration_values:
            if not isinstance(enumeration_value, ApixEnumerationValue):
                raise TypeError("Each element of the argument 'enumeration_values' must be an ApixEnumerationValue")

        if gql_enumeration_type_description is not None:
            if not isinstance(gql_enumeration_type_description, str):
                raise TypeError("The argument 'gql_enumeration_type_description' must be a string")

        return super().__new__(mcs, name, (ApixEnumerationElement,), **kwargs)

    def __init__(
            cls,
            name: str,
            enumeration_values: List[ApixEnumerationValue],
            *,
            gql_enumeration_type_description: str = None,
            **kwargs,
    ):

        super().__init__(name, (ApixEnumerationElement,), **kwargs)

        cls.enumeration_values = enumeration_values
        cls.gql_enumeration_type_description = gql_enumeration_type_description
        cls._kwargs = kwargs

        cls.enumeration_elements: List[ApixEnumerationElement] = []

        for enumeration_value in cls.enumeration_values:
            enumeration_element = cls(enumeration_value.value)
            cls.enumeration_elements.append(enumeration_element)
            setattr(cls, enumeration_element.class_name, enumeration_element)

    @cached_property
    def attribute(cls) -> ApixAttribute | None:
        return None

    @cached_property
    def attributes(cls) -> List[ApixAttribute]:
        return []

    @cached_property
    def kwargs(cls) -> Dict[str, Any]:

        return {
            'name': cls._name,
            'enumeration_values': cls.enumeration_values,
            'gql_enumeration_type_description': cls.gql_enumeration_type_description,
            **cls._kwargs,
        }

    @cached_property
    def gql_input_type(cls) -> GraphQLEnumType:
        return cls.gql_enumeration_type

    @cached_property
    def gql_output_type(cls) -> GraphQLEnumType:
        return cls.gql_enumeration_type

    def from_value(cls, value: Any) -> ApixEnumerationAttribute:
        return cls(value)

    def to_input(cls, value: Any) -> Any:
        return value.value

    def resolve_gql_output_field(
            cls,
            source: ApixDocument | ApixObjectAttribute,
            _: GraphQLResolveInfo,
    ) -> Any:

        value = getattr(source, cls.name, None)

        if value is not None:
            return value.value

    @cached_property
    def enumeration_values_by_value(cls) -> Dict[Any, ApixEnumerationValue]:
        return {enumeration_value.value: enumeration_value for enumeration_value in cls.enumeration_values}

    @cached_property
    def gql_enumeration_type(cls) -> GraphQLEnumType:

        return GraphQLEnumType(
            name=cls.class_path_name,
            values={enumeration_value.class_name: enumeration_value.gql_enumeration_value for enumeration_value in cls.enumeration_values},
            description=cls.gql_enumeration_type_description,
        )


class ApixListAttribute(ApixAttribute):

    def __new__(
            mcs,
            name: str,
            attribute: ApixAttribute | Callable[[], ApixAttribute],
            **kwargs,
    ):

        if isinstance(attribute, ApixAttribute):
            pass
        elif callable(attribute):
            if len(signature(attribute).parameters) > 0:
                raise ValueError("The argument 'attribute' must be a function with no argument")
        else:
            raise TypeError("The argument 'attribute' must be an ApixAttribute or a function")

        return super().__new__(mcs, name, (), **kwargs)

    def __init__(
            cls,
            name: str,
            attribute: ApixAttribute | Callable[[], ApixAttribute],
            **kwargs,
    ):

        super().__init__(name, (), **kwargs)

        cls._attribute = attribute
        cls._kwargs = kwargs
        cls._elements = {}

        cls.AnyIsNull = ApixAnyIsNullComparisonType(cls)
        cls.AnyEqual = ApixAnyEqualComparisonType(cls)
        cls.AnyNotEqual = ApixAnyNotEqualComparisonType(cls)
        cls.AnyLessThan = ApixAnyLessThanComparisonType(cls)
        cls.AnyLessThanEqual = ApixAnyLessThanEqualComparisonType(cls)
        cls.AnyGreaterThan = ApixAnyGreaterThanComparisonType(cls)
        cls.AnyGreaterThanEqual = ApixAnyGreaterThanEqualComparisonType(cls)
        cls.AnyIn = ApixAnyInComparisonType(cls)
        cls.AnyNotIn = ApixAnyNotInComparisonType(cls)

        cls.Push = ApixPushOperationType(cls)
        cls.Pop = ApixPopOperationType(cls)

    def __call__(cls, *args) -> List:
        return [cls.attribute.from_value(value) for value in args]

    def __getitem__(
            cls,
            index: int,
    ) -> ApixAttribute:

        if not isinstance(index, int):
            raise TypeError('Index must be an integer')

        if not index >= 0:
            raise ValueError('Index must not be negative')

        if index not in cls._elements:
            attribute_copy = cls.attribute.copy()
            attribute_copy._model = cls.model
            attribute_copy._parent = cls
            attribute_copy._index = index
            cls._elements[index] = attribute_copy

        return cls._elements.get(index)

    @cached_property
    def attribute(cls) -> ApixAttribute | None:

        if is_lambda_function(cls._attribute):
            cls._attribute = cls._attribute()

        cls._attribute._model = cls.model
        cls._attribute._parent = cls

        return cls._attribute

    @cached_property
    def attributes(cls) -> List[ApixAttribute]:

        attributes = []

        for attribute in cls.attribute.attributes:
            attribute_copy = attribute.copy()
            attribute_copy._model = cls.model
            attribute_copy._parent = cls
            attributes.append(attribute_copy)

        return attributes

    @cached_property
    def kwargs(cls) -> Dict[str, Any]:

        return {
            'name': cls._name,
            'attribute': cls.attribute.copy(),
            **cls._kwargs
        }

    def from_value(cls, value: Any) -> List:
        if isinstance(value, list):
            return cls(*value)
        else:
            return cls(value)

    def to_input(cls, value: Any) -> Any:
        return [cls.attribute.to_input(val) for val in value]

    @cached_property
    def gql_input_type(cls) -> GraphQLList:
        return GraphQLList(cls.attribute.gql_wrapped_input_type)

    @cached_property
    def gql_output_type(cls) -> GraphQLList:
        return GraphQLList(cls.attribute.gql_wrapped_output_type)

    @cached_property
    def gql_element_comparison_type_fields(cls) -> Dict[str, GraphQLInputField]:

        fields = {'index': GraphQLInputField(GraphQLNonNull(GraphQLInt))}
        fields.update(cls[0].gql_comparison_type_fields)

        return fields

    @cached_property
    def gql_element_comparison_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls[0].class_path_name}Comparison',
            fields=cls.gql_element_comparison_type_fields,
            description=None,
            out_type=cls.gql_element_comparison_out_type,
        )

    def gql_element_comparison_out_type(
            cls,
            value,
    ) -> List[ApixComparison]:

        index = value.pop('index')
        return cls[index].gql_comparison_out_type(value)

    @cached_property
    def gql_element_comparison_field(cls) -> GraphQLInputField:
        return GraphQLInputField(GraphQLList(GraphQLNonNull(cls.gql_element_comparison_type)))

    @cached_property
    def gql_element_operation_type_fields(cls) -> Dict[str, GraphQLInputField]:

        fields = {'index': GraphQLInputField(GraphQLNonNull(GraphQLInt))}
        fields.update(cls[0].gql_operation_type_fields)

        return fields

    @cached_property
    def gql_element_operation_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls[0].class_path_name}Operation',
            fields=cls.gql_element_operation_type_fields,
            description=None,
            out_type=cls.gql_element_operation_out_type,
        )

    def gql_element_operation_out_type(
            cls,
            value,
    ) -> List[ApixOperation]:

        index = value.pop('index')
        return cls[index].gql_operation_out_type(value)

    @cached_property
    def gql_element_operation_field(cls) -> GraphQLInputField:
        return GraphQLInputField(GraphQLList(GraphQLNonNull(cls.gql_element_operation_type)))

    @cached_property
    def gql_element_direction_type_fields(cls) -> Dict[str, GraphQLInputField]:

        fields = {'index': GraphQLInputField(GraphQLNonNull(GraphQLInt))}
        fields.update(cls[0].gql_direction_type_fields)

        return fields

    @cached_property
    def gql_element_direction_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls[0].class_path_name}Direction',
            fields=cls.gql_element_direction_type_fields,
            description=None,
            out_type=cls.gql_element_direction_out_type,
        )

    def gql_element_direction_out_type(
            cls,
            value,
    ) -> List[Tuple[int, ApixDirection]]:

        index = value.pop('index')
        return cls[index].gql_direction_out_type(value)

    @cached_property
    def gql_element_direction_field(cls) -> GraphQLInputField:
        return GraphQLInputField(GraphQLList(GraphQLNonNull(cls.gql_element_direction_type)))


class ApixObjectAttribute(ApixAttribute):

    def __new__(
            mcs,
            name: str,
            attributes: List[ApixAttribute] | Callable[[], List[ApixAttribute]],
            *,
            gql_output_type_description: str = None,
            gql_input_type_description: str = None,
            **kwargs,
    ):

        if isinstance(attributes, list):
            for attribute in attributes:
                if not isinstance(attribute, ApixAttribute):
                    raise TypeError("Each element of the argument 'attributes' must be an ApixAttribute")
        elif callable(attributes):
            if len(signature(attributes).parameters) > 0:
                raise ValueError("The argument 'attributes' must be a function with no argument")
        else:
            raise TypeError("The argument 'attributes' must be a list or a function")

        if gql_output_type_description is not None:
            if not isinstance(gql_output_type_description, str):
                raise TypeError("The argument 'gql_output_type_description' must be a string")

        if gql_input_type_description is not None:
            if not isinstance(gql_input_type_description, str):
                raise TypeError("The argument 'gql_input_type_description' must be a string")

        return super().__new__(mcs, name, (ApixDocument,), **kwargs)

    def __init__(
            cls,
            name: str,
            attributes: List[ApixAttribute] | Callable[[], List[ApixAttribute]],
            *,
            gql_output_type_description: str = None,
            gql_input_type_description: str = None,
            **kwargs,
    ):

        super().__init__(name, (ApixDocument,), **kwargs)
        cls._attributes = attributes
        cls.gql_output_type_description = gql_output_type_description
        cls.gql_input_type_description = gql_input_type_description
        cls._kwargs = kwargs

    @cached_property
    def attribute(cls) -> ApixAttribute | None:
        return None

    @cached_property
    def attributes(cls) -> List[ApixAttribute]:

        if is_lambda_function(cls._attributes):
            cls._attributes = cls._attributes()

        for attribute in cls._attributes:
            attribute._model = cls.model
            attribute._parent = cls

        return cls._attributes

    @cached_property
    def kwargs(cls) -> Dict[str, Any]:

        return {
            'name': cls._name,
            'attributes': [attribute.copy() for attribute in cls.attributes],
            'gql_output_type_description': cls.gql_output_type_description,
            'gql_input_type_description': cls.gql_input_type_description,
            **cls._kwargs,
        }

    @cached_property
    def gql_input_type(cls) -> GraphQLInputObjectType:

        return GraphQLInputObjectType(
            name=f'{cls.class_path_name}Input',
            fields={attribute.field_name: attribute.gql_input_field for attribute in cls.attributes if attribute.gql_input_included},
            description=cls.gql_input_type_description,
            out_type=cls.gql_input_out_type,
        )

    @cached_property
    def gql_output_type(cls) -> GraphQLObjectType:

        return GraphQLObjectType(
            name=cls.class_path_name,
            fields={attribute.field_name: attribute.gql_output_field for attribute in cls.attributes if attribute.gql_output_included},
            description=cls.gql_output_type_description,
        )

    def from_value(cls, value: Any) -> ApixObjectAttribute:

        if isinstance(value, cls):
            return value
        elif isinstance(value, dict):
            return cls(**value)
        else:
            return cls(value)

    def to_input(cls, value: Any) -> Any:

        input = {}

        for key, val in value.__dict__.items():
            attribute = cls.attributes_by_name.get(key)
            input[attribute.name] = attribute.to_input(val)

        return input

    def gql_input_out_type(cls, value: Dict) -> ApixObjectAttribute:
        return cls(**value)


class ApixReferenceAttribute(ApixAttribute):

    def __new__(
            mcs,
            name: str,
            reference: ApixModel | Callable[[], ApixModel],
            **kwargs,
    ):

        if reference.__class__.__name__ == 'ApixModel':   # workaround because the module apix.model cannot be imported due to circular dependencies
            pass
        elif callable(reference):
            if len(signature(reference).parameters) > 0:
                raise ValueError("The argument 'reference' must be a function with no arguments")
        else:
            raise TypeError("The argument 'reference' must be an ApixModel or a function")

        return super().__new__(mcs, name, (ApixDocument,), **kwargs)

    def __init__(
            cls,
            name: str,
            reference: ApixModel | Callable[[], ApixModel],
            **kwargs,
    ):

        super().__init__(name, (ApixDocument,), **kwargs)
        cls._reference = reference
        cls._kwargs = kwargs

    @cached_property
    def attribute(cls) -> ApixAttribute | None:
        return None

    @cached_property
    def attributes(cls) -> List[ApixAttribute]:

        attributes = []

        for attribute in cls.reference.attributes:
            attribute_copy = attribute.copy()
            attribute_copy._parent = cls
            attribute_copy._model = cls.model
            attributes.append(attribute_copy)

        return attributes

    @cached_property
    def kwargs(cls) -> Dict[str, Any]:

        return {
            'name': cls._name,
            'reference': cls.reference,
            **cls._kwargs,
        }

    @cached_property
    def gql_input_type(cls) -> GraphQLScalarType:
        return GraphQLID

    @cached_property
    def gql_output_type(cls) -> GraphQLObjectType:
        return cls.reference.gql_output_type

    def from_value(cls, value: Any) -> ApixReferenceAttribute:

        if isinstance(value, cls):
            return value
        elif isinstance(value, dict):
            return cls(**value)
        else:
            return cls(id=value)

    def to_input(cls, value: Any) -> Any:
        return value.id

    @cached_property
    def reference(cls) -> ApixModel:

        if is_lambda_function(cls._reference):
            cls._reference = cls._reference()

        return cls._reference
