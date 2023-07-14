from __future__ import annotations

from typing import Dict, List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.model import *
    from apix.direction import *


__all__ = [
    'ApixOrder',
]


class ApixOrder:
    model: ApixModel

    def __new__(cls, *args: ApixDirection):
        return super().__new__(cls)

    def __init__(self, *args:  ApixDirection):
        self.directions = list(args)

    def __repr__(self) -> str:
        return f'<{self.model.name}:order>'

    @property
    def order(self) -> List[Tuple]:
        return [(direction.attribute.path_name, direction.value) for direction in self.directions]

    @property
    def pipeline(self) -> List[Dict]:
        return [{'$sort': {direction.attribute.path_name: direction.value for direction in self.directions}}]
