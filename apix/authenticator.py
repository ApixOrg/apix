from __future__ import annotations

from inspect import isawaitable, signature
from typing import Awaitable, Callable, TYPE_CHECKING

from apix.model import *
from apix.token import *


if TYPE_CHECKING:
    from apix.document import *


__all__ = [
    'ApixAuthenticator'
]


class ApixAuthenticator:

    def __new__(
            cls,
            model: ApixModel,
            authenticate: Callable[[ApixToken], ApixDocument | Awaitable[ApixDocument] | None | Awaitable[None]],
    ):

        if not isinstance(model, ApixModel):
            raise TypeError("The argument 'model' must be an ApixModel")

        if not callable(authenticate):
            raise TypeError("The argument 'authenticate' must be a function")
        elif len(signature(authenticate).parameters) != 1:
            raise TypeError("The argument 'authenticate' must be a function with exactly one argument")

        return super().__new__(cls)

    def __init__(
            self,
            model: ApixModel,
            authenticate: Callable[[ApixToken], ApixDocument | Awaitable[ApixDocument] | None | Awaitable[None]],
    ):

        self.model = model
        self._authenticate = authenticate

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}:{self.model.class_name}>'

    async def authenticate(self, token: ApixToken) -> ApixDocument | None:

        document = self._authenticate(token)

        if isawaitable(document):
            document = await document

        if document:
            if isinstance(document, self.model):
                return document # noqa
            else:
                raise TypeError(f"The 'authenticate' function must return a document of type {self.model}")
