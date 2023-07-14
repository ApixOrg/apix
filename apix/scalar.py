from datetime import datetime
from typing import Union

from bson import ObjectId


__all__ = [
    'ApixScalar',
    'ApixId',
    'ApixString',
    'ApixInteger',
    'ApixFloat',
    'ApixBoolean',
    'ApixDateTime',
]


ApixId = ObjectId
ApixString = str
ApixInteger = int
ApixFloat = float
ApixBoolean = bool
ApixDateTime = datetime

ApixScalar = Union[ApixId, ApixString, ApixInteger, ApixFloat, ApixBoolean, ApixDateTime]
