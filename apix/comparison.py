from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from apix.operator import *


if TYPE_CHECKING:
    from apix.attribute import *


__all__ = [
    'ApixComparison',
    'ApixValueComparison',
    'ApixValuesComparison',
    'ApixAnyValueComparison',
    'ApixAnyValuesComparison',
    'ApixIsNullComparison',
    'ApixIsNotNullComparison',
    'ApixEqualComparison',
    'ApixNotEqualComparison',
    'ApixLessThanComparison',
    'ApixLessThanEqualComparison',
    'ApixGreaterThanComparison',
    'ApixGreaterThanEqualComparison',
    'ApixInComparison',
    'ApixNotInComparison',
    'ApixAnyIsNullComparison',
    'ApixAnyIsNotNullComparison',
    'ApixAnyEqualComparison',
    'ApixAnyNotEqualComparison',
    'ApixAnyLessThanComparison',
    'ApixAnyLessThanEqualComparison',
    'ApixAnyGreaterThanComparison',
    'ApixAnyGreaterThanEqualComparison',
    'ApixAnyInComparison',
    'ApixAnyNotInComparison',
]


class ApixComparison:
    name: str
    attribute: ApixAttribute

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @property
    def condition(self) -> Dict:
        raise NotImplementedError


class ApixIsNullComparison(ApixComparison):

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {'$eq': None}}


class ApixIsNotNullComparison(ApixComparison):

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {'$ne': None}}


class ApixValueComparison(ApixComparison):
    operator: ApixComparisonOperator

    def __init__(self, value: Any):
        self.value = self.attribute.from_value(value)

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}:{self.value}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {self.operator.value: self.attribute.to_input(self.value)}}


class ApixValuesComparison(ApixComparison):
    operator: ApixComparisonOperator

    def __init__(self, *args: Any):
        self.values = [self.attribute.from_value(value) for value in args]

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}:{self.values}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {self.operator.value: [self.attribute.to_input(value) for value in self.values]}}


class ApixAnyIsNullComparison(ApixComparison):

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {'$elemMatch': {'$eq': None}}}


class ApixAnyIsNotNullComparison(ApixComparison):

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {'$elemMatch': {'$ne': None}}}


class ApixAnyValueComparison(ApixComparison):
    operator: ApixComparisonOperator

    def __init__(self, value: Any):
        self.value = self.attribute.attribute.from_value(value)

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}:{self.value}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {'$elemMatch': {self.operator.value: self.attribute.attribute.to_input(self.value)}}}


class ApixAnyValuesComparison(ApixComparison):
    operator: ApixComparisonOperator

    def __init__(self, *args: Any):
        self.values = [self.attribute.attribute.from_value(value) for value in args]

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}:{self.values}>'

    @property
    def condition(self) -> Dict:
        return {self.attribute.path_name: {'$elemMatch': {self.operator.value: [self.attribute.attribute.to_input(value) for value in self.values]}}}


class ApixEqualComparison(ApixValueComparison):
    pass


class ApixNotEqualComparison(ApixValueComparison):
    pass


class ApixLessThanComparison(ApixValueComparison):
    pass


class ApixLessThanEqualComparison(ApixValueComparison):
    pass


class ApixGreaterThanComparison(ApixValueComparison):
    pass


class ApixGreaterThanEqualComparison(ApixValueComparison):
    pass


class ApixInComparison(ApixValuesComparison):
    pass


class ApixNotInComparison(ApixValuesComparison):
    pass


class ApixAnyEqualComparison(ApixAnyValueComparison):
    pass


class ApixAnyNotEqualComparison(ApixAnyValueComparison):
    pass


class ApixAnyLessThanComparison(ApixAnyValueComparison):
    pass


class ApixAnyLessThanEqualComparison(ApixAnyValueComparison):
    pass


class ApixAnyGreaterThanComparison(ApixAnyValueComparison):
    pass


class ApixAnyGreaterThanEqualComparison(ApixAnyValueComparison):
    pass


class ApixAnyInComparison(ApixAnyValuesComparison):
    pass


class ApixAnyNotInComparison(ApixAnyValuesComparison):
    pass
