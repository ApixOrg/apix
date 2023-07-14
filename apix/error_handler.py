from __future__ import annotations

from typing import Callable, Type, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.error import *


__all__ = [
    'ApixErrorHandler',
]


class ApixErrorHandler:

    def __init__(
            self,
            error: Type[Exception],
            handle: Callable[[Exception], ApixError],
    ):

        self.error = error
        self.handle = handle

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}:{self.error.__name__}>'
