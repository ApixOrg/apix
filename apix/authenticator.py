from __future__ import annotations

from inspect import isawaitable
from typing import Awaitable, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.document import *
    from apix.model import *


__all__ = [
    'ApixAuthenticator'
]


class ApixAuthenticator:

    def __init__(self,
                 model: ApixModel,
                 authenticate: Callable[[str], ApixDocument | Awaitable[ApixDocument] | None | Awaitable[None]]):

        self.model = model
        self._authenticate = authenticate

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}:{self.model.class_name}>'

    async def authenticate(self, token: str) -> ApixDocument | None:

        document = self._authenticate(token)

        if isawaitable(document):
            document = await document

        if document:
            if isinstance(document, self.model):
                return document # noqa
            else:
                raise TypeError(f'The authenticator must return a document of type {self.model}')
