from __future__ import annotations

from typing import TYPE_CHECKING

from apix.cursor import *


if TYPE_CHECKING:
    from apix.model import *


__all__ = [
    'ApixCursorType',
    'ApixAsyncCursorType',
]


class ApixCursorType(type):

    def __new__(mcs, model: ApixModel):
        return super().__new__(mcs, ApixCursor.__name__, (ApixCursor,), {})

    def __init__(cls, model: ApixModel):

        super().__init__(ApixCursor.__name__, (ApixCursor,), {})
        cls.model = model

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.model.class_name}>'


class ApixAsyncCursorType(type):

    def __new__(mcs, model: ApixModel):
        return super().__new__(mcs, ApixAsyncCursor.__name__, (ApixAsyncCursor,), {})

    def __init__(cls, model: ApixModel):

        super().__init__(ApixAsyncCursor.__name__, (ApixAsyncCursor,), {})
        cls.model = model

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.model.class_name}>'
