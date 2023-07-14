from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.client_session import ClientSession


__all__ = [
    'ApixSession',
    'ApixAsyncSession',
]


ApixSession = ClientSession
ApixAsyncSession = AsyncIOMotorClientSession
