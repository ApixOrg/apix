import pytest

from apix.attribute import *
from apix.database import *
from apix.enumeration import *
from apix.error import *
from apix.error_handler import *
from apix.model import *


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


def test_valid_1_apix_enumeration_value():
    ApixEnumerationValue('some_name', 0, 'some description')


def test_valid_2_apix_enumeration_value():
    ApixEnumerationValue('some_name', 0)


def test_invalid_name_1_apix_enumeration_value():
    with pytest.raises(TypeError):
        ApixEnumerationValue(0, 0)


def test_invalid_name_2_apix_enumeration_value():
    with pytest.raises(ValueError):
        ApixEnumerationValue('Some name', 0)


def test_invalid_value_apix_enumeration_value():
    with pytest.raises(TypeError):
        ApixEnumerationValue('some_name', 1.1)


def test_invalid_description_apix_enumeration_value():
    with pytest.raises(TypeError):
        ApixEnumerationValue('some_name', 0, 0)


def test_valid_apix_id_attribute():
    ApixIdAttribute('some_id')


def test_invalid_name_1_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute(1)


def test_invalid_name_2_apix_id_attribute():
    with pytest.raises(ValueError):
        ApixIdAttribute('SomeId')


def test_invalid_gql_output_included_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_output_included='yes')


def test_invalid_gql_output_nullable_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_output_nullable='yes')


def test_invalid_gql_output_field_description_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_output_field_description=True)


def test_invalid_gql_input_included_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_input_included='yes')


def test_invalid_gql_input_nullable_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_input_nullable='yes')


def test_invalid_gql_input_field_description_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_input_field_description=True)


def test_invalid_gql_update_included_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_update_included='yes')


def test_invalid_gql_filter_included_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_filter_included='yes')


def test_invalid_gql_order_included_apix_id_attribute():
    with pytest.raises(TypeError):
        ApixIdAttribute('some_id', gql_order_included='yes')


def test_valid_apix_enumeration_attribute():
    ApixEnumerationAttribute('some_enumeration', [ApixEnumerationValue('some_value', 0)])


def test_invalid_enumeration_values_1_apix_enumeration_attribute():
    with pytest.raises(TypeError):
        ApixEnumerationAttribute('some_enumeration', 'some_value')


def test_invalid_enumeration_values_2_apix_enumeration_attribute():
    with pytest.raises(TypeError):
        ApixEnumerationAttribute('some_enumeration', ['some_value'])


def test_invalid_gql_enumeration_type_description_apix_enumeration_attribute():
    with pytest.raises(TypeError):
        ApixEnumerationAttribute('some_enumeration', [ApixEnumerationValue('some_value', 0)], gql_enumeration_type_description=0)


def test_valid_1_apix_list_attribute():
    ApixListAttribute('some_list', ApixIdAttribute('some_id'))


def test_valid_2_apix_list_attribute():
    ApixListAttribute('some_list', lambda: ApixIdAttribute('some_id'))


def test_invalid_attribute_1_apix_list_attribute():
    with pytest.raises(TypeError):
        ApixListAttribute('some_list', 'some_id')


def test_invalid_attribute_2_apix_list_attribute():
    with pytest.raises(ValueError):
        ApixListAttribute('some_list', lambda x: ApixIdAttribute('some_id'))


def test_valid_1_apix_object_attribute():
    ApixObjectAttribute('some_list', [ApixIdAttribute('some_id')])


def test_valid_2_apix_object_attribute():
    ApixObjectAttribute('some_list', lambda: [ApixIdAttribute('some_id')])


def test_invalid_attributes_1_apix_object_attribute():
    with pytest.raises(TypeError):
        ApixObjectAttribute('some_list', ['some_id'])


def test_invalid_attributes_2_apix_list_attribute():
    with pytest.raises(ValueError):
        ApixObjectAttribute('some_list', lambda x: [ApixIdAttribute('some_id')])


def test_invalid_gql_output_type_description_apix_object_attribute():
    with pytest.raises(TypeError):
        ApixObjectAttribute('some_list', [ApixIdAttribute('some_id')], gql_output_type_description=0)


def test_invalid_gql_input_type_description_apix_object_attribute():
    with pytest.raises(TypeError):
        ApixObjectAttribute('some_list', [ApixIdAttribute('some_id')], gql_input_type_description=0)


def test_valid_1_apix_reference_attribute():
    ApixReferenceAttribute('some_list', ApixModel('some_model', []))


def test_valid_2_apix_reference_attribute():
    ApixReferenceAttribute('some_list', lambda: ApixModel('some_model', []))


def test_invalid_reference_1_apix_reference_attribute():
    with pytest.raises(TypeError):
        ApixReferenceAttribute('some_list', 'some_model')


def test_invalid_reference_2_apix_reference_attribute():
    with pytest.raises(ValueError):
        ApixReferenceAttribute('some_list', lambda x: ApixModel('some_model', []))


def test_valid_1_apix_model():
    ApixModel('some_model', [ApixIdAttribute('some_id')])


def test_valid_2_apix_model():
    ApixModel('some_model', lambda: [ApixIdAttribute('some_id')])


def test_invalid_name_1_apix_model():
    with pytest.raises(TypeError):
        ApixModel(0, [ApixIdAttribute('some_id')])


def test_invalid_name_2_apix_model():
    with pytest.raises(ValueError):
        ApixModel('SomeName', [ApixIdAttribute('some_id')])


def test_invalid_attributes_1_apix_model():
    with pytest.raises(TypeError):
        ApixModel('some_model', ['some_id'])


def test_invalid_attributes_2_apix_model():
    with pytest.raises(ValueError):
        ApixModel('some_model', lambda x: [ApixIdAttribute('some_id')])


def test_invalid_gql_output_type_description_apix_model():
    with pytest.raises(TypeError):
        ApixModel('some_name', [ApixIdAttribute('some_id')], gql_output_type_description=0)


def test_invalid_gql_input_type_description_apix_model():
    with pytest.raises(TypeError):
        ApixModel('some_name', [ApixIdAttribute('some_id')], gql_input_type_description=0)


def test_invalid_gql_update_type_description_apix_model():
    with pytest.raises(TypeError):
        ApixModel('some_name', [ApixIdAttribute('some_id')], gql_update_type_description=0)


def test_invalid_gql_filter_type_description_apix_model():
    with pytest.raises(TypeError):
        ApixModel('some_name', [ApixIdAttribute('some_id')], gql_filter_type_description=0)


def test_invalid_gql_order_type_description_apix_model():
    with pytest.raises(TypeError):
        ApixModel('some_name', [ApixIdAttribute('some_id')], gql_order_type_description=0)
