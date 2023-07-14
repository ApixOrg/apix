from __future__ import annotations

from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorCommandCursor
    from pymongo.command_cursor import CommandCursor

    from apix.model import *
    from apix.document import *


__all__ = [
    'ApixCursor',
    'ApixAsyncCursor',
]


class ApixCursor:
    model: ApixModel

    def __init__(self, cursor: CommandCursor):
        self._cursor = cursor

    def __repr__(self) -> str:
        return f'<{self.model.name}:cursor>'

    def __iter__(self):
        return self

    def __next__(self) -> ApixDocument:

        kwargs = next(self._cursor)
        return self.model(**kwargs)

    def list(self) -> List[ApixDocument]:
        return list(self)


class ApixAsyncCursor:
    model: ApixModel

    def __init__(self, cursor: AsyncIOMotorCommandCursor):
        self._cursor = cursor

    def __repr__(self) -> str:
        return f'<{self.model.name}:async_cursor>'

    def __aiter__(self):
        return self

    async def __anext__(self) -> ApixDocument:

        kwargs = await anext(self._cursor)
        return self.model(**kwargs)

    async def list(self) -> List[ApixDocument]:
        return [document async for document in self] # noqa
