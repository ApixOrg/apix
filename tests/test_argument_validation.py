import pytest

from apix.database import *
from apix.error import *
from apix.error_handler import *


def test_valid_1_apix_error():
    ApixError('Some message', 'SOME_CODE')


def test_valid_2_apix_error():
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
    with pytest.raises(ValueError):
        ApixErrorHandler(ZeroDivisionError, lambda error1, error2: ApixError('Some message'))


def test_valid_apix_database():
    ApixDatabase('connection_string', 'database_name')


def test_valid_apix_database():
    ApixDatabase('connection_string', 'database_name')


def test_invalid_host_apix_database():
    with pytest.raises(TypeError):
        ApixDatabase(0, 'database_name')


def test_invalid_name_1_apix_database():
    with pytest.raises(TypeError):
        ApixDatabase('connection_string', 0)


def test_invalid_name_2_apix_database():
    with pytest.raises(ValueError):
        ApixDatabase('connection_string', 'DatabaseName')


def test_valid_apix_asyn_database():
    ApixAsyncDatabase('connection_string', 'database_name')


def test_invalid_host_apix_async_database():
    with pytest.raises(TypeError):
        ApixAsyncDatabase(0, 'database_name')


def test_invalid_name_1_apix_async_database():
    with pytest.raises(TypeError):
        ApixAsyncDatabase('connection_string', 0)


def test_invalid_name_2_apix_async_database():
    with pytest.raises(ValueError):
        ApixAsyncDatabase('connection_string', 'DatabaseName')
