from __future__ import annotations

from typing import Any

from apix.gql import *
from apix.utils import *


__all__ = [
    'ApixEnumerationValue',
    'ApixEnumerationElement',
]


class ApixEnumerationValue:

    def __init__(
            self,
            name: str,
            value: Any,
            description: str = None,
    ):

        self.name = name
        self.value = value
        self.description = description

    def __repr__(self):
        return f'<{self.__class__.__name__}:{self.class_name}>'

    @cached_property
    def class_name(self):
        return gql_snake_to_camel(self.name, True)

    @cached_property
    def gql_enumeration_value(self) -> GraphQLEnumValue:

        return GraphQLEnumValue(
            value=self.value,
            description=self.description,
        )


class ApixEnumerationElement(ApixEnumerationValue):

    def __new__(cls, value: Any):

        if cls is ApixEnumerationElement:
            raise TypeError('Cannot be instantiated')

        if value in cls.values_by_value: # noqa
            if value in cls.elements_by_value: # noqa
                return cls.elements_by_value.get(value) # noqa
            else:
                return super().__new__(cls)
        else:
            raise TypeError('Invalid value')

    def __init__(self, value: Any):

        value = self.__class__.values_by_value.get(value) # noqa
        super().__init__(value.name, value.value, value.description)
