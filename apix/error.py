from __future__ import annotations

from apix.gql import *


__all__ = [
    'ApixError',
]


class ApixError(GraphQLError):

    def __init__(
            self,
            message: str,
            code: str = 'UNSPECIFIED',
    ):

        super(ApixError, self).__init__(message, extensions={'code': code})
        self.code = code
