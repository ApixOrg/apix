from __future__ import annotations

from datetime import datetime
from inspect import isawaitable, signature, Parameter
from types import UnionType
from typing import Any, Callable, Dict, List, Optional, Union, get_origin, get_args, TYPE_CHECKING

from bson import ObjectId

from apix.gql import *
from apix.utils import *


if TYPE_CHECKING:
    from apix.app import *


__all__ = [
    'ApixResolver',
    'ApixQueryResolver',
    'ApixMutationResolver',
]


class ApixResolver:

    def __init__(
            self,
            function: Callable,
            description: str = None,
    ):

        self.function = function
        self.description = description

        self._app = None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}:{self.function.__name__}>'

    @cached_property
    def app(self) -> ApixApp | None:
        return self._app

    @cached_property
    def special_parameter_names(self) -> List[str]:
        return ['select', 'context']

    @cached_property
    def class_name(self) -> str:
        return gql_snake_to_camel(self.function.__name__, True)

    @cached_property
    def field_name(self) -> str:
        return gql_snake_to_camel(self.function.__name__, False)

    @cached_property
    def signature(self):
        return signature(self.function)

    @cached_property
    def parameters(self) -> List[Parameter]:
        return [parameter for parameter in self.signature.parameters.values()]

    @cached_property
    def parameters_by_name(self) -> Dict[str, Parameter]:
        return {parameter.name: parameter for parameter in self.parameters}

    @cached_property
    def gql_arguments(self) -> Dict[str, GraphQLArgument]:

        arguments = {}

        for parameter in self.parameters:
            if parameter.name not in self.special_parameter_names:
                arguments[parameter.name] = GraphQLArgument(
                    type_=self.map_parameter_to_gql_input_type(parameter),
                    default_value=Undefined if parameter.default is parameter.empty else parameter.default,
                )

        return arguments

    @cached_property
    def output_base(self) -> Any:
        try:
            return self.map_annotation_to_output_base(self.signature.return_annotation)
        except TypeError:
            raise TypeError(f'Invalid output type: {self.signature.return_annotation}')

    @cached_property
    def gql_output_type(self) -> GraphQLOutputType:
        try:
            return self.map_annotation_to_gql_output_type(self.signature.return_annotation)
        except TypeError:
            raise TypeError(f'Invalid output type: {self.signature.return_annotation}')

    @cached_property
    def gql_output_field(self) -> GraphQLField:

        return GraphQLField(
            type_=self.gql_output_type,
            args=self.gql_arguments,
            resolve=self.resolve,
            description=self.description,
        )

    async def resolve(
            self,
            _,
            gql_resolve_info: GraphQLResolveInfo,
            **kwargs,
    ) -> Any:

        if 'select' in self.parameters_by_name:
            kwargs['select'] = self.output_base.create_select_from_gql_resolve_info(gql_resolve_info)
        if 'context' in self.parameters_by_name:
            kwargs['context'] = gql_resolve_info.context

        try:
            result = self.function(**kwargs)

            if isawaitable(result):
                result = await result

        except Exception as error:
            raise self.app.handle_error(error)

        return result

    @staticmethod
    def is_optional_type(annotation: Any) -> bool:

        origin = get_origin(annotation)
        args = get_args(annotation)

        return origin in [Union, UnionType] and len(args) == 2 and type(None) != args[0] and type(None) == args[1]

    @staticmethod
    def is_list_type(annotation: Any) -> bool:

        origin = get_origin(annotation)
        args = get_args(annotation)

        return origin is list and len(args) == 1

    def map_annotation_to_output_base(
            self,
            annotation: Any,
    ) -> Any:

        if self.is_optional_type(annotation):
            return self._map_annotation_to_output_base(get_args(annotation)[0])
        else:
            return self._map_annotation_to_output_base(annotation)

    def _map_annotation_to_output_base(
            self,
            annotation: Any,
    ) -> Any:

        if self.is_list_type(annotation):
            return self.map_annotation_to_output_base(get_args(annotation)[0])
        else:
            return annotation

    def map_annotation_to_gql_output_type(
            self,
            annotation: Any,
    ) -> GraphQLOutputType:

        if self.is_optional_type(annotation):
            return self._map_annotation_to_gql_output_type(get_args(annotation)[0])
        else:
            return GraphQLNonNull(self._map_annotation_to_gql_output_type(annotation))

    def _map_annotation_to_gql_output_type(
            self,
            annotation: Any,
    ) -> GraphQLOutputType:

        if self.is_list_type(annotation):
            return GraphQLList(self.map_annotation_to_gql_output_type(get_args(annotation)[0]))
        elif annotation is ObjectId:
            return GraphQLID
        elif annotation is str:
            return GraphQLString
        elif annotation is int:
            return GraphQLInt
        elif annotation is float:
            return GraphQLFloat
        elif annotation is bool:
            return GraphQLBoolean
        elif annotation is datetime:
            return GraphQLDateTime
        elif hasattr(annotation, 'gql_output_type'):
            return annotation.gql_output_type
        else:
            raise TypeError('Invalid annotation type')

    def map_parameter_to_gql_input_type(self, parameter: Parameter):

        if parameter.default is parameter.empty:
            if self.is_optional_type(parameter.annotation):
                raise TypeError('An optional argument must have a default value.')

        annotation = parameter.annotation

        if parameter is not parameter.empty and not self.is_optional_type(parameter):
            annotation = Optional[annotation]

        try:
            return self.map_annotation_to_gql_input_type(annotation)
        except TypeError:
            raise TypeError(f'Invalid argument type: {parameter.annotation}')

    def map_annotation_to_gql_input_type(
            self,
            annotation: Any,
    ) -> GraphQLInputType:

        if self.is_optional_type(annotation):
            return self._map_annotation_to_gql_input_type(get_args(annotation)[0])
        else:
            return GraphQLNonNull(self._map_annotation_to_gql_input_type(annotation))

    def _map_annotation_to_gql_input_type(
            self,
            annotation: Any,
    ) -> GraphQLInputType:

        if self.is_list_type(annotation):
            return GraphQLList(self.map_annotation_to_gql_input_type(get_args(annotation)[0]))
        elif annotation is ObjectId:
            return GraphQLID
        elif annotation is str:
            return GraphQLString
        elif annotation is int:
            return GraphQLInt
        elif annotation is float:
            return GraphQLFloat
        elif annotation is bool:
            return GraphQLBoolean
        elif annotation is datetime:
            return GraphQLDateTime
        elif hasattr(annotation, 'gql_input_type'):
            return annotation.gql_input_type
        else:
            raise TypeError('Invalid annotation type')


class ApixQueryResolver(ApixResolver):
    pass


class ApixMutationResolver(ApixResolver):
    pass
