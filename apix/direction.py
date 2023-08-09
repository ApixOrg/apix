from __future__ import annotations

from typing import Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.attribute import *


__all__ = [
    'ApixDirection',
    'ApixAscendingDirection',
    'ApixDescendingDirection',
]


class ApixDirection:
    name: str
    attribute: ApixAttribute

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self) -> str:
        return f'<{self.attribute.name}:{self.name}>'

    @property
    def order(self) -> Tuple:
        raise NotImplementedError


class ApixAscendingDirection(ApixDirection):

    @property
    def order(self) -> Tuple:
        return self.attribute.path_name, 1


class ApixDescendingDirection(ApixDirection):

    @property
    def order(self) -> Tuple:
        return self.attribute.path_name, -1
