from functools import cache
from typing import Callable


__all__ = [
    'is_snake_case',
    'is_lambda_function',
    'cached_property',
]


def is_snake_case(x: str) -> bool:

    b1 = len(x) > 0
    b2 = x.islower()
    b3 = x.replace('_', '').isalpha()
    b4 = '__' not in x
    b5 = not x.startswith('_')
    b6 = not x.endswith('_')

    return b1 & b2 & b3 & b4 & b5 & b6


def is_lambda_function(function: Callable) -> bool:
    return callable(function) and function.__name__ == '<lambda>'


def cached_property(f: Callable) -> property:
    return property(cache(f))
