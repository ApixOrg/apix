from __future__ import annotations

from typing import Any, Type, TYPE_CHECKING

from apix.comparison import *
from apix.gql import *
from apix.operator import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.attribute import *


__all__ = [
    'ApixComparisonType',

    'ApixIsNullComparisonType',
    'ApixIsNotNullComparisonType',
    'ApixValueComparisonType',
    'ApixEqualComparisonType',
    'ApixNotEqualComparisonType',
    'ApixLessThanComparisonType',
    'ApixLessThanEqualComparisonType',
    'ApixGreaterThanComparisonType',
    'ApixGreaterThanEqualComparisonType',
    'ApixInComparisonType',
    'ApixNotInComparisonType',

    'ApixAnyIsNullComparisonType',
    'ApixAnyIsNotNullComparisonType',
    'ApixAnyValueComparisonType',
    'ApixAnyEqualComparisonType',
    'ApixAnyNotEqualComparisonType',
    'ApixAnyLessThanComparisonType',
    'ApixAnyLessThanEqualComparisonType',
    'ApixAnyGreaterThanComparisonType',
    'ApixAnyGreaterThanEqualComparisonType',
    'ApixAnyInComparisonType',
    'ApixAnyNotInComparisonType',

]


class ApixComparisonType(type):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixComparison],
            attribute: ApixAttribute,
    ):

        return super().__new__(mcs, base.__name__, (base,), {})

    def __init__(
            cls,
            name: str,
            base: Type[ApixComparison],
            attribute: ApixAttribute,
    ):

        super().__init__(base.__name__, (base,), {})
        cls.name = name
        cls.attribute = attribute

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.attribute.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        raise NotImplementedError

    def from_value(cls, value: Any) -> ApixComparison:
        raise NotImplementedError

    @cached_property
    def field_name(cls) -> str:
        return gql_snake_to_camel(cls.name, False)

    @cached_property
    def gql_input_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_input_type,
            description=None,
        )


class ApixValueComparisonType(ApixComparisonType):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixValueComparison],
            attribute: ApixAttribute,
            operator: ApixComparisonOperator,
    ):

        return super().__new__(mcs, name, base, attribute)

    def __init__(
            cls,
            name: str,
            base: Type[ApixValueComparison],
            attribute: ApixAttribute,
            operator: ApixComparisonOperator,
    ):

        super().__init__(name, base, attribute)
        cls.operator = operator

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.gql_input_type

    def from_value(cls, value: Any) -> ApixComparison:
        return cls(value)


class ApixValuesComparisonType(ApixComparisonType):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixValuesComparison],
            attribute: ApixAttribute,
            operator: ApixComparisonOperator,
    ):

        return super().__new__(mcs, name, base, attribute)

    def __init__(
            cls,
            name: str,
            base: Type[ApixValuesComparison],
            attribute: ApixAttribute,
            operator: ApixComparisonOperator,
    ):

        super().__init__(name, base, attribute)
        cls.operator = operator

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return GraphQLList(cls.attribute.gql_input_type)

    def from_value(cls, value: Any) -> ApixComparison:

        if isinstance(value, list):
            return cls(*value)
        else:
            return cls(value)


class ApixAnyValueComparisonType(ApixComparisonType):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixAnyValueComparison],
            attribute: ApixListAttribute,
            operator: ApixComparisonOperator,
    ):

        return super().__new__(mcs, name, base, attribute)

    def __init__(
            cls,
            name: str,
            base: Type[ApixAnyValueComparison],
            attribute: ApixListAttribute,
            operator: ApixComparisonOperator,
    ):

        super().__init__(name, base, attribute)
        cls.operator = operator

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.attribute.gql_input_type

    def from_value(cls, value: Any) -> ApixComparisonType:
        return cls(value)


class ApixAnyValuesComparisonType(ApixComparisonType):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixAnyValuesComparison],
            attribute: ApixListAttribute,
            operator: ApixComparisonOperator,
    ):

        return super().__new__(mcs, name, base, attribute)

    def __init__(
            cls,
            name: str,
            base: Type[ApixAnyValuesComparison],
            attribute: ApixListAttribute,
            operator: ApixComparisonOperator,
    ):

        super().__init__(name, base, attribute)
        cls.operator = operator

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return GraphQLList(cls.attribute.attribute.gql_input_type)

    def from_value(cls, value: Any) -> ApixComparisonType:

        if isinstance(value, list):
            return cls(*value)
        else:
            return cls(value)


class ApixIsNullComparisonType(ApixComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'is_null', ApixIsNullComparison, attribute)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('is_null', ApixIsNullComparison, attribute)

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.gql_input_type

    def from_value(cls, value: Any) -> ApixComparisonType:
        return cls(value)


class ApixIsNotNullComparisonType(ApixComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'is_not_null', ApixIsNotNullComparison, attribute)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('is_not_null', ApixIsNotNullComparison, attribute)

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.gql_input_type

    def from_value(cls, value: Any) -> ApixComparisonType:
        return cls(value)


class ApixEqualComparisonType(ApixValueComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'equal', ApixEqualComparison, attribute, ApixComparisonOperator.EQUAL)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('equal', ApixEqualComparison, attribute, ApixComparisonOperator.EQUAL)


class ApixNotEqualComparisonType(ApixValueComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'not_equal', ApixNotEqualComparison, attribute, ApixComparisonOperator.NOT_EQUAL)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('not_equal', ApixNotEqualComparison, attribute, ApixComparisonOperator.NOT_EQUAL)


class ApixLessThanComparisonType(ApixValueComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'less_than', ApixLessThanComparison, attribute, ApixComparisonOperator.LESS_THAN)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('less_than', ApixLessThanComparison, attribute, ApixComparisonOperator.LESS_THAN)


class ApixLessThanEqualComparisonType(ApixValueComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'less_than_equal', ApixLessThanEqualComparison, attribute, ApixComparisonOperator.LESS_THAN_EQUAL)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('less_than_equal', ApixLessThanEqualComparison, attribute, ApixComparisonOperator.LESS_THAN_EQUAL)


class ApixGreaterThanComparisonType(ApixValueComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'greater_than', ApixGreaterThanComparison, attribute, ApixComparisonOperator.GREATER_THAN)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('greater_than', ApixGreaterThanComparison, attribute, ApixComparisonOperator.GREATER_THAN)


class ApixGreaterThanEqualComparisonType(ApixValueComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'greater_than_equal', ApixGreaterThanEqualComparison, attribute, ApixComparisonOperator.GREATER_THAN_EQUAL)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('greater_than_equal', ApixGreaterThanEqualComparison, attribute, ApixComparisonOperator.GREATER_THAN_EQUAL)


class ApixInComparisonType(ApixValuesComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'in', ApixInComparison, attribute, ApixComparisonOperator.IN)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('in', ApixInComparison, attribute, ApixComparisonOperator.IN)


class ApixNotInComparisonType(ApixValuesComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'not_in', ApixNotInComparison, attribute, ApixComparisonOperator.NOT_IN)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('not_in', ApixNotInComparison, attribute, ApixComparisonOperator.NOT_IN)


class ApixAnyIsNullComparisonType(ApixComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'any_is_null', ApixAnyIsNullComparison, attribute)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('any_is_null', ApixAnyIsNullComparison, attribute)

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.attribute.gql_input_type

    def from_value(cls, value: Any) -> ApixComparisonType:
        return cls(value)


class ApixAnyIsNotNullComparisonType(ApixComparisonType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'any_is_not_null', ApixAnyIsNotNullComparison, attribute)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('any_is_not_null', ApixAnyIsNotNullComparison, attribute)

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.attribute.gql_input_type

    def from_value(cls, value: Any) -> ApixComparisonType:
        return cls(value)


class ApixAnyEqualComparisonType(ApixAnyValueComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_equal', ApixAnyEqualComparison, attribute, ApixComparisonOperator.EQUAL)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_equal', ApixAnyEqualComparison, attribute, ApixComparisonOperator.EQUAL)


class ApixAnyNotEqualComparisonType(ApixAnyValueComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_not_equal', ApixAnyNotEqualComparison, attribute, ApixComparisonOperator.NOT_EQUAL)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_not_equal', ApixAnyNotEqualComparison, attribute, ApixComparisonOperator.NOT_EQUAL)


class ApixAnyLessThanComparisonType(ApixAnyValueComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_less_than', ApixAnyLessThanComparison, attribute, ApixComparisonOperator.LESS_THAN)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_less_than', ApixAnyLessThanComparison, attribute, ApixComparisonOperator.LESS_THAN)


class ApixAnyLessThanEqualComparisonType(ApixAnyValueComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_less_than_equal', ApixAnyLessThanEqualComparison, attribute, ApixComparisonOperator.LESS_THAN_EQUAL)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_less_than_equal', ApixAnyLessThanEqualComparison, attribute, ApixComparisonOperator.LESS_THAN_EQUAL)


class ApixAnyGreaterThanComparisonType(ApixAnyValueComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_greater_than', ApixAnyGreaterThanComparison, attribute, ApixComparisonOperator.GREATER_THAN)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_greater_than', ApixAnyGreaterThanComparison, attribute, ApixComparisonOperator.GREATER_THAN)


class ApixAnyGreaterThanEqualComparisonType(ApixAnyValueComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_greater_than_equal', ApixAnyGreaterThanEqualComparison, attribute, ApixComparisonOperator.GREATER_THAN_EQUAL)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_greater_than_equal', ApixAnyGreaterThanEqualComparison, attribute, ApixComparisonOperator.GREATER_THAN_EQUAL)


class ApixAnyInComparisonType(ApixAnyValuesComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_in', ApixAnyInComparison, attribute, ApixComparisonOperator.IN)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_in', ApixAnyInComparison, attribute, ApixComparisonOperator.IN)


class ApixAnyNotInComparisonType(ApixAnyValuesComparisonType):

    def __new__(mcs, attribute: ApixListAttribute):
        return super().__new__(mcs, 'any_not_in', ApixAnyNotInComparison, attribute, ApixComparisonOperator.NOT_IN)

    def __init__(cls, attribute: ApixListAttribute):
        super().__init__('any_not_in', ApixAnyNotInComparison, attribute, ApixComparisonOperator.NOT_IN)
