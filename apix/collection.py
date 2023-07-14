from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING

from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorCollection

from apix.attribute import *
from apix.comparison import *
from apix.direction import *
from apix.document import *
from apix.filter import *
from apix.order import *
from apix.scalar import *
from apix.select import *
from apix.session import *
from apix.update import *


if TYPE_CHECKING:
    from apix.cursor import *
    from apix.model import *
    from apix.operation import *


__all__ = [
    'ApixCollection',
    'ApixAsyncCollection',
]


class ApixCollection:

    def __init__(
            self,
            model: ApixModel,
    ):

        self.model = model

    def __repr__(self) -> str:
        return f'<{self.__class__.__base__.__name__}:{self.model.class_name}>'

    @property
    def _collection(self) -> Collection:
        return Collection(self.__class__._database, self.model.name) # noqa

    @staticmethod
    def create_find_one_pipeline(
            filter: ApixFilter = None,
            select: ApixSelect = None,
    ) -> List[Dict]:

        pipeline = []

        if filter:
            pipeline += filter.pipeline

        if select:
            pipeline += select.pipeline

        pipeline += [{'$limit': 1}]

        return pipeline

    @staticmethod
    def create_find_many_pipeline(
            filter: ApixFilter = None,
            order: ApixOrder = None,
            skip: int = None,
            limit: int = None,
            select: ApixSelect = None,
    ) -> List[Dict]:

        pipeline = []

        if filter:
            pipeline += filter.pipeline

        if order:
            pipeline += order.pipeline

        if skip:
            pipeline += [{'$skip': skip}]

        if limit:
            pipeline += [{'$limit': limit}]

        if select:
            pipeline += select.pipeline

        return pipeline

    def find_one_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            select: ApixSelect | ApixAttribute = None,
            session: ApixSession = None,
    ) -> ApixDocument | None:

        if isinstance(filter, ApixComparison):
            filter = self.model.Filter(filter)

        if isinstance(select, ApixAttribute):
            select = self.model.Select(select)

        pipeline = self.create_find_one_pipeline(filter, select)
        cursor = self._collection.aggregate(pipeline, session=session)

        for document in self.model.Cursor(cursor):
            return document

    def find_one(
            self,
            filter: ApixFilter | ApixComparison = None,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixDocument | None:

        return self.find_one_in_session(filter, select)

    def find_by_id_in_session(
            self,
            id: ApixId,
            select: ApixSelect | ApixAttribute = None,
            session: ApixSession = None,
    ):
        return self.find_one_in_session(self.model.Id.Equal(id), select, session)

    def find_by_id(
            self,
            id: ApixId,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixDocument | None:

        return self.find_by_id_in_session(id, select)

    def find_many_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            order: ApixOrder | ApixDirection = None,
            skip: int = None,
            limit: int = None,
            select: ApixSelect | ApixAttribute = None,
            session: ApixSession = None,
    ) -> ApixCursor:

        if isinstance(filter, ApixComparison):
            filter = self.model.Filter(filter)

        if isinstance(order, ApixDirection):
            order = self.model.Order(order)

        if isinstance(select, ApixAttribute):
            select = self.model.Select(select)

        pipeline = self.create_find_many_pipeline(filter, order, skip, limit, select)
        cursor = self._collection.aggregate(pipeline, session=session)

        return self.model.Cursor(cursor)

    def find_many(
            self,
            filter: ApixFilter = None,
            order: ApixOrder | ApixDirection = None,
            skip: int = None,
            limit: int = None,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixCursor:
        return self.find_many_in_session(filter, order, skip, limit, select)

    def find_by_ids_in_session(
            self,
            ids: List[ApixId],
            order: ApixOrder | ApixDirection = None,
            select: ApixSelect | ApixAttribute = None,
            session: ApixSession = None,
    ) -> ApixCursor:

        return self.find_many_in_session(self.model.Id.In(*ids), order, None, None, select, session)

    def find_by_ids(
            self,
            ids: List[ApixId],
            order: ApixOrder | ApixDirection = None,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixCursor:

        return self.find_by_ids_in_session(ids, order, select)

    def insert_one_in_session(
            self,
            document: ApixDocument,
            session: ApixSession = None,
    ) -> None:

        cursor = self._collection.insert_one(
            document=self.model.to_input(document),
            session=session,
        )

        document.id = cursor.inserted_id

    def insert_one(
            self,
            document: ApixDocument,
    ) -> None:
        self.insert_one_in_session(document)

    def insert_many_in_session(
            self,
            documents: List[ApixDocument],
            session: ApixSession = None,
    ) -> None:

        cursor = self._collection.insert_many(
            documents=[self.model.to_input(document) for document in documents],
            session=session,
        )

        for (inserted_id, document) in zip(cursor.inserted_ids, documents):
            document.id = inserted_id

    def insert_many(
            self,
            documents: List[ApixDocument],
    ) -> None:
        self.insert_many_in_session(documents)

    def update_one_in_session(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
            session: ApixSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        self._collection.update_one(
            filter=filter.condition,
            update=update.update,
            session=session,
        )

    def update_one(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
    ) -> None:
        self.update_one_in_session(update, filter)

    def update_by_id_in_session(
            self,
            id: ApixId,
            update: ApixUpdate | ApixOperation,
            session: ApixSession = None,
    ) -> None:
        self.update_one_in_session(update, self.model.Id.Equal(id), session)

    def update_by_id(
            self,
            id: ApixId,
            update: ApixUpdate | ApixOperation,
    ) -> None:
        self.update_by_id_in_session(id, update)

    def update_many_in_session(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
            session: ApixSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        self._collection.update_many(
            filter=filter.condition,
            update=update.update,
            session=session,
        )

    def update_many(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
    ) -> None:

        self.update_many_in_session(update, filter)

    def update_by_ids_in_session(
            self,
            ids: List[ApixId],
            update: ApixUpdate | ApixOperation,
            session: ApixSession = None,
    ) -> None:

        self.update_many_in_session(update, self.model.Id.In(*ids), session)

    def update_by_ids(
            self,
            ids: List[ApixId],
            update: ApixUpdate | ApixOperation,
    ) -> None:

        self.update_by_ids_in_session(ids, update)

    def delete_one_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            session: ApixSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        self._collection.delete_one(
            filter=filter.condition,
            session=session,
        )

    def delete_one(
            self,
            filter: ApixFilter = None,
    ) -> None:

        self.delete_one_in_session(filter)

    def delete_by_id_in_session(
            self,
            id: ApixId,
            session: ApixSession = None,
    ) -> None:

        self.delete_one_in_session(self.model.Id.Equal(id), session)

    def delete_by_id(
            self,
            id: ApixId,
    ) -> None:

        self.delete_by_id_in_session(id)

    def delete_many_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            session: ApixSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        self._collection.delete_many(
            filter=filter.condition,
            session=session,
        )

    def delete_many(
            self,
            filter: ApixFilter | ApixComparison = None,
    ) -> None:

        self.delete_many_in_session(filter)

    def delete_by_ids_in_session(
            self,
            ids: List[ApixId],
            session: ApixSession = None,
    ) -> None:

        self.delete_many_in_session(self.model.Id.In(*ids), session)

    def delete_by_ids(
            self,
            ids: List[ApixId],
    ) -> None:

        self.delete_by_ids_in_session(ids)

    def replace_one(
            self,
            document: ApixDocument,
            upsert: bool = False,
    ) -> None:

        if hasattr(document, 'id'):

            self._collection.replace_one(
                filter=self.model.Id.Equal(document.id).condition,
                replacement=self.model.to_input(document),
                upsert=upsert,
            )


class ApixAsyncCollection:

    def __init__(
            self,
            model: ApixModel,
    ):

        self.model = model

    def __repr__(self) -> str:
        return f'<{self.__class__.__base__.__name__}:{self.model.class_name}>'

    @property
    def _collection(self) -> AsyncIOMotorCollection:
        return AsyncIOMotorCollection(self.__class__._database, self.model.name) # noqa

    @staticmethod
    def create_find_one_pipeline(
            filter: ApixFilter = None,
            select: ApixSelect = None,
    ) -> List[Dict]:

        return ApixCollection.create_find_one_pipeline(filter, select)

    @staticmethod
    def create_find_many_pipeline(
            filter: ApixFilter = None,
            order: ApixOrder = None,
            skip: int = None,
            limit: int = None,
            select: ApixSelect = None,
    ) -> List[Dict]:

        return ApixCollection.create_find_many_pipeline(filter, order, skip, limit, select)

    async def find_one_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            select: ApixSelect | ApixAttribute = None,
            session: ApixAsyncSession = None,
    ) -> ApixDocument | None:

        if isinstance(filter, ApixComparison):
            filter = self.model.Filter(filter)

        if isinstance(select, ApixAttribute):
            select = self.model.Select(select)

        pipeline = self.create_find_one_pipeline(filter, select)
        cursor = self._collection.aggregate(pipeline, session=session)

        async for document in self.model.AsyncCursor(cursor):
            return document

    async def find_one(
            self,
            filter: ApixFilter | ApixComparison = None,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixDocument | None:

        return await self.find_one_in_session(filter, select)

    async def find_by_id_in_session(
            self,
            id: ApixId,
            select: ApixSelect | ApixAttribute = None,
            session: ApixAsyncSession = None,
    ) -> ApixDocument | None:
        return await self.find_one_in_session(self.model.Id.Equal(id), select, session)

    async def find_by_id(
            self,
            id: ApixId,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixDocument | None:

        return await self.find_by_id_in_session(id, select)

    def find_many_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            order: ApixOrder | ApixDirection = None,
            skip: int = None,
            limit: int = None,
            select: ApixSelect | ApixAttribute = None,
            session: ApixAsyncSession = None,
    ) -> ApixAsyncCursor:

        pipeline = self.create_find_many_pipeline(filter, order, skip, limit, select)
        cursor = self._collection.aggregate(pipeline, session=session)

        return self.model.AsyncCursor(cursor)

    def find_many(
            self,
            filter: ApixFilter | ApixComparison = None,
            order: ApixOrder | ApixDirection = None,
            skip: int = None,
            limit: int = None,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixAsyncCursor:

        return self.find_many_in_session(filter, order, skip, limit, select)

    def find_by_ids_in_session(
            self,
            ids: List[ApixId],
            order: ApixOrder | ApixDirection = None,
            select: ApixSelect | ApixAttribute = None,
            session: ApixAsyncSession = None,
    ) -> ApixAsyncCursor:
        return self.find_many_in_session(self.model.Id.In(ids), order, None, None, select, session)

    def find_by_ids(
            self,
            ids: List[ApixId],
            order: ApixOrder | ApixDirection = None,
            select: ApixSelect | ApixAttribute = None,
    ) -> ApixAsyncCursor:
        return self.find_by_ids_in_session(ids, order, select)

    async def insert_one_in_session(
            self,
            document: ApixDocument,
            session: ApixAsyncSession = None,
    ) -> None:

        cursor = await self._collection.insert_one(
            document=document.__apix_input__,
            session=session,
        )

        document.id = cursor.inserted_id

    async def insert_one(
            self,
            document: ApixDocument,
    ) -> None:

        await self.insert_one_in_session(document)

    async def insert_many_in_session(
            self,
            documents: List[ApixDocument],
            session: ApixAsyncSession = None,
    ) -> None:

        cursor = await self._collection.insert_many(
            documents=[self.model.to_input(document) for document in documents],
            session=session,
        )

        for (inserted_id, document) in zip(cursor.inserted_ids, documents):
            document.id = inserted_id

    async def insert_many(
            self,
            documents: List[ApixDocument],
    ) -> None:

        await self.insert_many_in_session(documents)

    async def update_one_in_session(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
            session: ApixAsyncSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        await self._collection.update_one(
            filter=filter.condition,
            update=update.update,
            session=session,
        )

    async def update_one(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
    ) -> None:

        await self.update_one_in_session(update, filter)

    async def update_by_id_in_session(
            self,
            id: ApixId,
            update: ApixUpdate | ApixOperation,
            session: ApixAsyncSession = None,
    ) -> None:

        await self.update_one_in_session(update, self.model.Id.Equal(id), session)

    async def update_by_id(
            self,
            id: ApixId,
            update: ApixUpdate | ApixOperation,
    ) -> None:

        await self.update_by_id_in_session(id, update)

    async def update_many_in_session(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
            session: ApixAsyncSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        await self._collection.update_many(
            filter=filter.condition,
            update=update.update,
            session=session,
        )

    async def update_many(
            self,
            update: ApixUpdate | ApixOperation,
            filter: ApixFilter | ApixComparison = None,
    ) -> None:

        await self.update_many_in_session(update, filter)

    async def update_by_ids_in_session(
            self,
            ids: List[ApixId],
            update: ApixUpdate | ApixOperation,
            session: ApixAsyncSession = None,
    ) -> None:

        await self.update_many_in_session(update, self.model.Id.In(*ids), session)

    async def update_by_ids(
            self,
            ids: List[ApixId],
            update: ApixUpdate | ApixOperation,
    ) -> None:

        await self.update_by_ids_in_session(ids, update)

    async def delete_one_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            session: ApixAsyncSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        await self._collection.delete_one(
            filter=filter.condition,
            session=session,
        )

    async def delete_one(
            self,
            filter: ApixFilter = None,
    ) -> None:

        await self.delete_one_in_session(filter)

    async def delete_by_id_in_session(
            self,
            id: ApixId,
            session: ApixAsyncSession = None,
    ) -> None:

        await self.delete_one_in_session(self.model.Id.Equal(id), session)

    async def delete_by_id(
            self,
            id: ApixId,
    ) -> None:

        await self.delete_by_id_in_session(id)

    async def delete_many_in_session(
            self,
            filter: ApixFilter | ApixComparison = None,
            session: ApixAsyncSession = None,
    ) -> None:

        if not filter:
            filter = self.model.Filter()

        await self._collection.delete_many(
            filter=filter.condition,
            session=session,
        )

    async def delete_many(
            self,
            filter: ApixFilter | ApixComparison = None,
    ) -> None:

        await self.delete_many_in_session(filter)

    async def delete_by_ids_in_session(
            self,
            ids: List[ApixId],
            session: ApixAsyncSession = None,
    ) -> None:

        await self.delete_many_in_session(self.model.Id.In(*ids), session)

    async def delete_by_ids(
            self,
            ids: List[ApixId],
    ) -> None:

        await self.delete_by_ids_in_session(ids)
