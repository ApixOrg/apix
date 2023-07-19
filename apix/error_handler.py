from __future__ import annotations

from inspect import signature
from typing import Callable, Type, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.error import *


__all__ = [
    'ApixErrorHandler',
]


class ApixErrorHandler:

    def __new__(
            cls,
            error_type: Type[Exception],
            handle: Callable[[Exception], ApixError],
    ):

        if not issubclass(error_type, Exception):
            raise TypeError("The argument 'error' must be a subclass of Exception")

        if not callable(handle):
            raise TypeError("The argument 'handle' must be a function")
        elif len(signature(handle).parameters) != 1:
            raise TypeError("The argument 'handle' must be a function with exactly one argument")

        return super().__new__(cls)

    def __init__(
            self,
            error_type: Type[Exception],
            handle: Callable[[Exception], ApixError],
    ):

        self.error_type = error_type
        self._handle = handle

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}:{self.error_type.__name__}>'

    def handle(self, error: Exception) -> ApixError:

        apix_error = self._handle(error)

        if not isinstance(apix_error, ApixError):
            raise TypeError(f"The 'handle' function must return an ApixError")

        return apix_error
