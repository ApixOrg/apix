from __future__ import annotations

from enum import Enum


__all__ = [
    'ApixToken',
    'ApixTokenType',
]


class ApixTokenType(Enum):
    BASIC = 'basic'
    BEARER = 'bearer'


class ApixToken:

    def __init__(
            self,
            type: ApixTokenType,
            value: str,
    ):

        self.type = type
        self.value = value

    @staticmethod
    def from_string(string: str) -> ApixToken | None:

        lower_string = string.lower()

        if lower_string.startswith('basic '):

            return ApixToken(
                type=ApixTokenType.BASIC,
                value=string[6:],
            )

        elif lower_string.startswith('bearer '):

            return ApixToken(
                type=ApixTokenType.BEARER,
                value=string[7:],
            )
