from __future__ import annotations

from typing import TYPE_CHECKING

from apix.select import *


if TYPE_CHECKING:
    from apix.model import *


__all__ = [
    'ApixSelectType',
]


class ApixSelectType(type):

    def __new__(mcs, model: ApixModel):
        return super().__new__(mcs, ApixSelect.__name__, (ApixSelect,), {})

    def __init__(cls, model: ApixModel):

        super().__init__(ApixSelect.__name__, (ApixSelect,), {})
        cls.model = model

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.model.class_name}>'
