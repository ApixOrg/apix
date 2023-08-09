from enum import Enum

from apix.gql import *


__all__ = [
    'ApixComparisonOperator',

    'ApixUpdateOperator',

    'ApixLogicalOperator',
    'ApixLogicalOperatorEnumType',
    'ApixLogicalOperatorInputField',

    'ApixDirectionOperator',
    'ApixDirectionOperatorEnumType',
    'ApixDirectionOperatorInputField',
]


class ApixLogicalOperator(Enum):
    AND = '$and'
    OR = '$or'
    NOR = '$nor'


class ApixComparisonOperator(Enum):
    EQUAL = '$eq'
    NOT_EQUAL = '$ne'
    LESS_THAN = '$lt'
    LESS_THAN_EQUAL = '$lte'
    GREATER_THAN = '$gt'
    GREATER_THAN_EQUAL = '$gte'
    IN = '$in'
    NOT_IN = '$nin'


class ApixUpdateOperator(Enum):
    SET = '$set'
    UNSET = '$unset'
    INCREMENT = '$inc'
    MULTIPLY = '$mul'
    MIN = '$min'
    MAX = '$max'
    PUSH = '$push'
    POP = '$pop'


class ApixDirectionOperator(Enum):
    ASCENDING = 1
    DESCENDING = 0


ApixLogicalOperatorEnumType = GraphQLEnumType(
    name='LogicalOperator',
    values={key: GraphQLEnumValue(value) for key, value in ApixLogicalOperator.__members__.items()},
    description=None,
)


ApixLogicalOperatorInputField = GraphQLInputField(
    type_=GraphQLNonNull(ApixLogicalOperatorEnumType),
    default_value=ApixLogicalOperator.AND,
    out_name='operator',
)


ApixDirectionOperatorEnumType = GraphQLEnumType(
    name='DirectionOperator',
    values={key: GraphQLEnumValue(value) for key, value in ApixDirectionOperator.__members__.items()}
)


ApixDirectionOperatorInputField = GraphQLInputField(
    type_=GraphQLNonNull(ApixDirectionOperatorEnumType),
    default_value=ApixDirectionOperator.ASCENDING,
)
