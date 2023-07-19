import pytest

from apix.error import *
from apix.error_handler import *


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


def test_valid_apix_error_handler():
    ApixErrorHandler(ZeroDivisionError, lambda error: ApixError('Some message'))


def test_invalid_error_type_apix_error_handler():
    with pytest.raises(TypeError):
        ApixErrorHandler(ZeroDivisionError(), lambda error: ApixError('Some message'))


def test_invalid_handle_1_apix_error_handler():
    with pytest.raises(TypeError):
        ApixErrorHandler(ZeroDivisionError, None)


def test_invalid_handle_2_apix_error_handler():
    with pytest.raises(TypeError):
        ApixErrorHandler(ZeroDivisionError, lambda error1, error2: ApixError('Some message'))
