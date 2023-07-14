from __future__ import annotations

from datetime import datetime
from typing import Dict, TYPE_CHECKING
from uuid import uuid4


if TYPE_CHECKING:
    from apix.document import ApixDocument


__all__ = [
    'ApixContext',
]


class ApixContext:

    def __init__(
            self,
            request_id: uuid4,
            requested_at: datetime,
            requested_by: ApixDocument = None,
    ):

        self.request_id = request_id
        self.requested_at = requested_at
        self.requested_by = requested_by

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}:{self.request_id}>'

    @property
    def extensions(self) -> Dict:

        return {
            'requestId': str(self.request_id),
            'requestedAt': self.requested_at.isoformat(),
            'requestedBy': str(self.requested_by.id) if hasattr(self.requested_by, 'id') else None
        }
