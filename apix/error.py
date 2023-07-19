from __future__ import annotations

from apix.gql import *


__all__ = [
    'ApixError',
]


class ApixError(GraphQLError):

    def __new__(
            cls,
            message: str,
            code: str = 'UNSPECIFIED',
    ):

        if not isinstance(message, str):
            raise TypeError("The argument 'message' must be a string")

        if not isinstance(code, str):
            raise TypeError("The argument 'code' must be a string")

        return super().__new__(cls)

    def __init__(
            self,
            message: str,
            code: str = 'UNSPECIFIED',
    ):

        super(ApixError, self).__init__(message, extensions={'code': code})
        self.code = code
