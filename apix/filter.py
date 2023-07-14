from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING

from apix.comparison import *
from apix.operator import *


if TYPE_CHECKING:
    from apix.model import *


__all__ = [
    'ApixFilter',
]


class ApixFilter:
    model: ApixModel

    def __new__(
            cls,
            *args: ApixComparison,
            operator: ApixLogicalOperator = ApixLogicalOperator.AND,
    ):
        return super().__new__(cls)

    def __init__(
            self,
            *args: ApixComparison,
            operator: ApixLogicalOperator = ApixLogicalOperator.AND,
    ):

        self.operator = operator
        self.comparisons = list(args)

    def __repr__(self) -> str:
        return f'<{self.model.name}:filter>'

    @property
    def condition(self) -> Dict:
        if self.comparisons:
            return {self.operator.value: [comparison.condition for comparison in self.comparisons]}
        else:
            return {}

    @property
    def pipeline(self) -> List[Dict]:
        return [{'$match': self.condition}]
