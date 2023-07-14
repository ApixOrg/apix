import datetime
import json
from typing import Any

from bson.objectid import ObjectId, InvalidId
from graphql import (
    ExecutionResult,

    DocumentNode,
    FieldNode,
    ValueNode,
    StringValueNode,
    print_ast,

    GraphQLOutputType,
    GraphQLInputType,
    GraphQLWrappingType,

    GraphQLResolveInfo,
    GraphQLSchema,
    GraphQLArgument,
    GraphQLObjectType,

    GraphQLInputObjectType,
    GraphQLScalarType,
    GraphQLField,
    GraphQLInputField,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLList,
    GraphQLNonNull,
    GraphQLError,

    GraphQLString,
    GraphQLInt,
    GraphQLFloat,
    GraphQLBoolean,

    Undefined,

    parse as gql_parse,
    validate as gql_validate,
    execute as gql_execute,
    parse_value as gql_parse_value,
    value_from_ast as gql_value_from_ast,
)
from graphql.pyutils import snake_to_camel as gql_snake_to_camel


__all__ = [
    'ExecutionResult',

    'DocumentNode',
    'FieldNode',
    'ValueNode',

    'GraphQLOutputType',
    'GraphQLInputType',
    'GraphQLWrappingType',

    'GraphQLResolveInfo',
    'GraphQLSchema',
    'GraphQLArgument',

    'GraphQLObjectType',
    'GraphQLInputObjectType',
    'GraphQLScalarType',
    'GraphQLField',
    'GraphQLInputField',
    'GraphQLEnumType',
    'GraphQLEnumValue',
    'GraphQLList',
    'GraphQLNonNull',
    'GraphQLError',

    'GraphQLID',
    'GraphQLString',
    'GraphQLInt',
    'GraphQLFloat',
    'GraphQLBoolean',
    'GraphQLDateTime',

    'Undefined',

    'gql_parse',
    'gql_validate',
    'gql_execute',
    'gql_parse_value',
    'gql_value_from_ast',
    'gql_snake_to_camel',
]


def _serialize_id(output_value: Any) -> str:
    if isinstance(output_value, ObjectId):
        return str(ObjectId(output_value))
    else:
        raise output_value.GraphQLError(f'ID cannot be converted to a 24-character hex string: {output_value}')


def _coerce_id(input_value: Any) -> ObjectId:
    try:
        return ObjectId(input_value)
    except (InvalidId, TypeError):
        raise GraphQLError(f'ID must be a 24-character hex string: {input_value}')


def _parse_id_literal(value_node: ValueNode, _variables: Any = None) -> ObjectId:
    """Parse an ID value node in the AST."""
    try:
        if not isinstance(value_node, StringValueNode):
            raise TypeError
        return ObjectId(value_node.value)
    except (InvalidId, TypeError):
        raise GraphQLError(f'ID must be a 24-character hex string: {print_ast(value_node)}', value_node)


def _serialize_date_time(output_value: Any) -> str:
    if type(output_value) == datetime.datetime:
        return output_value.isoformat()
    else:
        raise GraphQLError(f'DateTime cannot be converted to an ISO 8601 formatted string: {output_value}')


def _coerce_date_time(input_value: Any) -> datetime:
    try:
        return datetime.datetime.fromisoformat(input_value)
    except (ValueError, TypeError):
        raise GraphQLError(f'DateTime must be an ISO 8601 formatted string: {input_value}')


def _parse_date_time_literal(value_node: ValueNode) -> datetime.datetime:
    try:
        if not isinstance(value_node, StringValueNode):
            raise TypeError
        return datetime.datetime.fromisoformat(value_node.value)
    except (ValueError, TypeError):
        raise GraphQLError(f'DateTime must be an ISO 8601 formatted string: {print_ast(value_node)}', value_node)


def _is_serializable_dictionary(value: Any) -> bool:

    try:
        json.dumps(value)
        return isinstance(value, dict)

    except TypeError:
        return False


GraphQLID = GraphQLScalarType(
    name='ID',
    description="The `ID` scalar type represents a unique identifier,"
                " often used to refetch an object or as key for a cache."
                " The ID type appears in a JSON response as a 24-character hex string."
                " When expected as an input type, any valid 24-character hex string will be accepted as an ID.",
    serialize=_serialize_id,
    parse_value=_coerce_id,
    parse_literal=_parse_id_literal,
)


GraphQLDateTime = GraphQLScalarType(
    name='DateTime',
    description="The `DateTime` scalar type represents a timestamp in ISO 8601 standard."
                " The DateTime type appears in a JSON response as an IS0 8601 formatted String with time in Coordinated Universal Time (UTC)."
                " When expected as an input type, any valid IS0 8601 formatted string will be accepted as a DateTime.",
    serialize=_serialize_date_time,
    parse_value=_coerce_date_time,
    parse_literal=_parse_date_time_literal,
)
