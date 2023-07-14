from __future__ import annotations

from typing import Any, Dict, List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.attribute import *


__all__ = [
    'ApixDirection',
]


class ApixDirection:
    name: str
    attribute: ApixAttribute

    def __new__(cls, value: Any):
        return super().__new__(cls)

    def __init__(self, value: Any):
        self.value = 1 if bool(value) else -1

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:direction:{self.value_string}>'

    @property
    def value_string(self) -> str:
        return 'asc' if self.value else 'desc'

    @property
    def order(self) -> List[Tuple]:
        return [(self.attribute.path_name, self.value)]
