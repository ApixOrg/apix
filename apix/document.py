from __future__ import annotations

from typing import Any


__all__ = [
    'ApixDocument',
]


class ApixDocument:

    def __new__(cls, **kwargs: Any):
        return super().__new__(cls)

    def __init__(self, **kwargs: Any):

        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self) -> str:
        if hasattr(self, 'id'):
            return f'<{self.__class__.name}:{self.id}>' # noqa
        else:
            return f'<{self.__class__.name}>' # noqa

    def __setattr__(
            self,
            key: str,
            value: Any,
    ):

        if key == '_id':
            key = 'id'

        attribute = self.__class__.get_attribute_by_name(key) # noqa

        if attribute:
            if value is None:
                if hasattr(self, key):
                    super().__delattr__(key)
            else:
                super().__setattr__(key, attribute.from_value(value))

    def __getattr__(self, key: str):

        if key == '_id':
            key = 'id'

        return super().__getattribute__(key)
