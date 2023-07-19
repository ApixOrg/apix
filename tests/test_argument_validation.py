import pytest

from apix.error import *


def test_valid_apix_error():
    ApixError('Some message', 'SOME_CODE')


def test_valid_apix_error_without_code():
    ApixError('Some message')


def test_invalid_message_apix_error():
    with pytest.raises(TypeError):
        ApixError(0, 'SOME_CODE')


def test_invalid_code_apix_error():
    with pytest.raises(TypeError):
        ApixError('Some message', 0)
