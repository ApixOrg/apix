from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.attribute import *
    from apix.operator import *


__all__ = [
    'ApixOperation',
    'ApixValueOperation',
    'ApixUnsetOperation',
    'ApixSetOperation',
    'ApixIncrementOperation',
    'ApixMultiplyOperation',
    'ApixMinOperation',
    'ApixMaxOperation',
    'ApixPushOperation',
    'ApixPopOperation',
]


class ApixOperation:
    name: str
    attribute: ApixAttribute

    @property
    def update(self) -> Dict:
        raise NotImplementedError


class ApixUnsetOperation(ApixOperation):
    operator: ApixUpdateOperator

    def __init__(self, *args, **kwargs):
        pass

    @property
    def update(self):
        return {self.operator.value: {self.attribute.path_name: None}}


class ApixValueOperation(ApixOperation):
    operator: ApixUpdateOperator

    def __init__(self, value: Any):
        self.value = self.attribute.from_value(value)

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}:{self.value}>'

    @property
    def update(self):
        return {self.operator.value: {self.attribute.path_name: self.attribute.to_input(self.value)}}


class ApixSetOperation(ApixValueOperation):
    pass


class ApixIncrementOperation(ApixValueOperation):
    pass


class ApixMultiplyOperation(ApixValueOperation):
    pass


class ApixMinOperation(ApixValueOperation):
    pass


class ApixMaxOperation(ApixValueOperation):
    pass


class ApixPushOperation(ApixOperation):
    operator: ApixUpdateOperator

    def __init__(self, *args: Any):
        self.values = self.attribute.from_value(list(args))

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}:{self.values}>'

    @property
    def update(self):
        return {self.operator.value: {self.attribute.path_name: {'$each': self.attribute.to_input(self.values)}}}


class ApixPopOperation(ApixOperation):
    operator: ApixUpdateOperator

    def __init__(self, value: Any):
        self.value = 1 if bool(value) else -1

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}:{self.value}>'

    @property
    def update(self):
        return {self.operator.value: {self.attribute.path_name: self.value}}
