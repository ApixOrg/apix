from __future__ import annotations

from typing import Any

from apix.gql import *
from apix.utils import *


__all__ = [
    'ApixEnumerationValue',
    'ApixEnumerationElement',
]


class ApixEnumerationValue:

    def __new__(
            cls,
            name: str,
            value: str | int,
            gql_enumeration_value_description: str = None,
    ):

        if not isinstance(name, str):
            raise TypeError("The argument 'name' must be a string")
        elif not is_snake_case(name):
            raise ValueError("The argument 'name' must be snake case")

        if not isinstance(value, str) and not isinstance(value, int):
            raise TypeError("The argument 'value' must be a string or integer")

        if gql_enumeration_value_description is not None:
            if not isinstance(gql_enumeration_value_description, str):
                raise TypeError("The argument 'gql_enumeration_value_description' must be a string")

        return super().__new__(cls)

    def __init__(
            self,
            name: str,
            value: str | int,
            gql_enumeration_value_description: str = None,
    ):

        self.name = name
        self.value = value
        self.gql_enumeration_value_description = gql_enumeration_value_description

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self.class_name}>'

    @cached_property
    def class_name(self):
        return gql_snake_to_camel(self.name, True)

    @cached_property
    def field_name(self):
        return gql_snake_to_camel(self.name, False)

    @cached_property
    def gql_enumeration_value(self) -> GraphQLEnumValue:

        return GraphQLEnumValue(
            value=self.value,
            description=self.gql_enumeration_value_description,
        )


class ApixEnumerationElement(ApixEnumerationValue):

    def __new__(cls, value: Any):

        if value in cls.enumeration_elements: # noqa
            return value
        elif value in cls.enumeration_values_by_value: # noqa
            enumeration_value = cls.enumeration_values_by_value.get(value) # noqa
            return super().__new__(cls, enumeration_value.name, enumeration_value.value, enumeration_value.gql_enumeration_value_description)
        else:
            raise ValueError(f"'{value}' is not a valid {cls}")

    def __init__(self, value: Any):

        enumeration_value = self.__class__.enumeration_values_by_value.get(value) # noqa
        super().__init__(enumeration_value.name, enumeration_value.value, enumeration_value.gql_enumeration_value_description)
