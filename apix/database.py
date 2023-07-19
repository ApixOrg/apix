from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from apix.collection import *
from apix.gql import *
from apix.session import *
from apix.utils import *


__all__ = [
    'ApixDatabase',
    'ApixAsyncDatabase'
]


class ApixDatabase(type):

    def __new__(
            mcs,
            host: str,
            name: str,
    ):

        if not isinstance(host, str):
            raise TypeError("The argument 'host' must be a string")

        if not isinstance(name, str):
            raise TypeError("The argument 'name' must be a string")
        elif not is_snake_case(name):
            raise ValueError(f"The argument 'name' must be snake case.")

        return super().__new__(mcs, mcs.__name__, (ApixCollection,), {})

    def __init__(
            cls,
            host: str,
            name: str,
    ):

        super().__init__(cls.__name__, (ApixCollection,), {})
        cls.host = host
        cls.name = name

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.class_name}>'

    @cached_property
    def class_name(cls) -> str:
        return gql_snake_to_camel(cls.name, True)

    @cached_property
    def _client(cls) -> MongoClient:
        return MongoClient(cls.host)

    @cached_property
    def _database(cls) -> Database:
        return Database(cls._client, cls.name)

    def start_session(cls, causal_consistency: bool = None) -> ApixSession:
        return cls._client.start_session(causal_consistency)

    def close(cls) -> None:
        cls._client.close()


class ApixAsyncDatabase(type):

    def __new__(
            mcs,
            host: str,
            name: str,
    ):
        return super().__new__(mcs, mcs.__name__, (ApixAsyncCollection,), {})

    def __init__(
            cls,
            host: str,
            name: str,
    ):

        super().__init__(cls.__name__, (ApixAsyncCollection,), {})
        cls.host = host
        cls.name = name

    def __repr__(cls) -> str:
        return f'<{cls.__name__}:{cls.class_name}>'

    @cached_property
    def class_name(cls) -> str:
        return gql_snake_to_camel(cls.name, True)

    @cached_property
    def _client(cls) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(cls.host)

    @cached_property
    def _database(cls) -> AsyncIOMotorDatabase:
        return AsyncIOMotorDatabase(cls._client, cls.name)

    def start_session(cls, causal_consistency: bool = None) -> ApixAsyncSession:
        return cls._client.start_session(causal_consistency)

    def close(cls) -> None:
        cls._client.close()
