from __future__ import annotations

from typing import Any, Type, TYPE_CHECKING

from apix.gql import *
from apix.operation import *
from apix.operator import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.attribute import *


__all__ = [
    'ApixOperationType',
    'ApixValueOperationType',
    'ApixSetOperationType',
    'ApixUnsetOperationType',
    'ApixIncrementOperationType',
    'ApixMultiplyOperationType',
    'ApixMinOperationType',
    'ApixMaxOperationType',
    'ApixPushOperationType',
    'ApixPopOperationType',
]


class ApixOperationType(type):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixOperation],
            attribute: ApixAttribute,
    ):

        return super().__new__(mcs, mcs.__name__, (base,), {})

    def __init__(
            cls,
            name: str,
            base: Type[ApixOperation],
            attribute: ApixAttribute,
    ):

        super().__init__(cls.__name__, (base,), {})
        cls.name = name
        cls.attribute = attribute

    def __repr__(cls) -> str:
        return f'{cls.__name__}:{cls.attribute.class_name}'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        raise NotImplementedError

    def from_value(
            cls,
            value: Any,
    ) -> ApixOperation:
        raise NotImplementedError

    @cached_property
    def class_name(cls) -> str:
        return gql_snake_to_camel(cls.name, True)

    @cached_property
    def field_name(cls) -> str:
        return gql_snake_to_camel(cls.name, False)

    @cached_property
    def gql_input_field(cls) -> GraphQLInputField:

        return GraphQLInputField(
            type_=cls.gql_input_type,
            description=None,
        )


class ApixValueOperationType(ApixOperationType):

    def __new__(
            mcs,
            name: str,
            base: Type[ApixValueOperation],
            attribute: ApixAttribute,
            operator: ApixUpdateOperator,
    ):

        return super().__new__(mcs, name, base, attribute)

    def __init__(
            cls,
            name: str,
            base: Type[ApixValueOperation],
            attribute: ApixAttribute,
            operator: ApixUpdateOperator,
    ):

        super().__init__(name, base, attribute)
        cls.operator = operator

    def __repr__(self) -> str:
        return f'<{self.base.__name__}:{self.attribute.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.gql_input_type

    def from_value(
            cls,
            value: Any,
    ) -> ApixOperation:

        return cls(value)


class ApixSetOperationType(ApixValueOperationType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'set', ApixSetOperation, attribute, ApixUpdateOperator.SET)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('set', ApixSetOperation, attribute, ApixUpdateOperator.SET)


class ApixUnsetOperationType(ApixValueOperationType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'unset', ApixUnsetOperation, attribute, ApixUpdateOperator.UNSET)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('unset', ApixUnsetOperation, attribute, ApixUpdateOperator.UNSET)


class ApixIncrementOperationType(ApixValueOperationType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'increment', ApixIncrementOperation, attribute, ApixUpdateOperator.INCREMENT)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('increment', ApixIncrementOperation, attribute, ApixUpdateOperator.INCREMENT)


class ApixMultiplyOperationType(ApixValueOperationType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'multiply', ApixMultiplyOperation, attribute, ApixUpdateOperator.MULTIPLY)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('multiply', ApixMultiplyOperation, attribute, ApixUpdateOperator.MULTIPLY)


class ApixMinOperationType(ApixValueOperationType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'min', ApixMinOperation, attribute, ApixUpdateOperator.MIN)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('min', ApixMinOperation, attribute, ApixUpdateOperator.MIN)


class ApixMaxOperationType(ApixValueOperationType):

    def __new__(mcs, attribute: ApixAttribute):
        return super().__new__(mcs, 'max', ApixMaxOperation, attribute, ApixUpdateOperator.MAX)

    def __init__(cls, attribute: ApixAttribute):
        super().__init__('max', ApixMaxOperation, attribute, ApixUpdateOperator.MAX)


class ApixPushOperationType(ApixOperationType):

    def __new__(
            mcs,
            attribute: ApixListAttribute,
    ):

        return super().__new__(mcs, 'push', ApixPushOperation, attribute)

    def __init__(
            cls,
            attribute: ApixListAttribute,
    ):

        super().__init__('push', ApixPushOperation, attribute)
        cls.operator = ApixUpdateOperator.PUSH

    def __repr__(self) -> str:
        return f'<{self.base.__name__}:{self.attribute.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return cls.attribute.gql_input_type

    def from_value(
            cls,
            value: Any,
    ) -> ApixOperation:

        if isinstance(value, list):
            return cls(*value)
        else:
            return cls(value)


class ApixPopOperationType(ApixOperationType):

    def __new__(
            mcs,
            attribute: ApixListAttribute,
    ):

        return super().__new__(mcs, 'pop', ApixPopOperation, attribute)

    def __init__(
            cls,
            attribute: ApixListAttribute,
    ):

        super().__init__('pop', ApixPopOperation, attribute)
        cls.operator = ApixUpdateOperator.POP

    def __repr__(self) -> str:
        return f'<{self.base.__name__}:{self.attribute.class_name}>'

    @cached_property
    def gql_input_type(cls) -> GraphQLInputType:
        return GraphQLBoolean

    def from_value(cls, value: Any) -> ApixOperation:
        return cls(value)
