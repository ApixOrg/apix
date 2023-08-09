from __future__ import annotations

from inspect import isawaitable, signature
from typing import Awaitable, Callable, TYPE_CHECKING

from apix.error import *
from apix.token import *


if TYPE_CHECKING:
    from apix.document import *


__all__ = [
    'ApixAuthenticator'
]


class ApixAuthenticator:

    def __new__(
            cls,
            authenticate: Callable[[ApixToken], ApixDocument | Awaitable[ApixDocument] | None | Awaitable[None]],
            error: ApixError,
    ):

        if not callable(authenticate):
            raise TypeError("The argument 'authenticate' must be a function")
        elif len(signature(authenticate).parameters) != 1:
            raise TypeError("The argument 'authenticate' must be a function with exactly one argument")

        if not isinstance(error, ApixError):
            raise TypeError("The argument 'error' must be an ApixError")

        return super().__new__(cls)

    def __init__(
            self,
            authenticate: Callable[[ApixToken], ApixDocument | Awaitable[ApixDocument] | None | Awaitable[None]],
            error: ApixError,
    ):

        self._authenticate = authenticate
        self.error = error

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}>'

    async def authenticate(self, token: ApixToken) -> ApixDocument | None:

        document = self._authenticate(token)

        if isawaitable(document):
            document = await document

        return document
