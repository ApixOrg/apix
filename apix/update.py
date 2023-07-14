from __future__ import annotations

from typing import Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.model import *
    from apix.operation import *


__all__ = [
    'ApixUpdate',
]


class ApixUpdate:
    model: ApixModel

    def __new__(cls, *args: ApixOperation):
        return super().__new__(cls)

    def __init__(self, *args: ApixOperation):
        self.operations = list(args)

    def __repr__(self) -> str:
        return f'<{self.model.name}:update>'

    @property
    def update(self) -> Dict:

        update = {}

        for operation in self.operations:
            for update_operator, value in operation.update.items():
                if update_operator not in update:
                    update[update_operator] = {}
                update[update_operator].update(value)

        return update
