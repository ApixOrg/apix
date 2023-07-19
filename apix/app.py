from __future__ import annotations

import inspect
import json
from datetime import datetime
from functools import cached_property
from typing import Dict, List, Type
from uuid import uuid4

from starlette.applications import Starlette, Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from apix.authenticator import *
from apix.context import *
from apix.error import *
from apix.error_handler import *
from apix.gql import *
from apix.resolver import *


__all__ = [
    'ApixApp',
]


class ApixApp(Starlette):

    def __new__(
            cls,
            resolvers: List[ApixResolver],
            *,
            authenticator: ApixAuthenticator = None,
            error_handlers: List[ApixErrorHandler] = None,
            gql_path: str = '/graphql',
            include_extensions: bool = False,
            **kwargs,
    ):

        if not isinstance(resolvers, list):
            raise TypeError("The argument 'resolvers' must be a list")
        else:
            for resolver in resolvers:
                if not isinstance(resolver, ApixResolver):
                    raise TypeError("Each element of the argument 'resolvers' must be an ApixResolver")

        if authenticator is not None:
            if not isinstance(authenticator, ApixAuthenticator):
                raise TypeError("The argument 'authenticator' must be an ApixAuthenticator")

        if error_handlers is not None:
            if not isinstance(error_handlers, list):
                raise TypeError("The argument 'error_handlers' must be a list")
            else:
                for error_handler in error_handlers:
                    if not isinstance(error_handler, ApixErrorHandler):
                        raise TypeError("Each element of the argument 'error_handlers' must be an ApixErrorHandler")

        if not isinstance(gql_path, str):
            raise TypeError("The argument 'gql_path' must be a string")

        if not isinstance(include_extensions, bool):
            raise TypeError("The argument 'include_extensions' must be a boolean")

        return super().__new__(cls)

    def __init__(
            self,
            resolvers: List[ApixResolver],
            *,
            authenticator: ApixAuthenticator = None,
            error_handlers: List[ApixErrorHandler] = None,
            gql_path: str = '/graphql',
            include_extensions: bool = False,
            **kwargs,
    ):

        for resolver in resolvers:
            resolver._app = self

        if not error_handlers:
            error_handlers = []

        self.resolvers = resolvers
        self.authenticator = authenticator
        self.error_handlers = error_handlers
        self.gql_path = gql_path
        self.include_extensions = include_extensions

        if 'routes' not in kwargs:
            kwargs['routes'] = []

        kwargs['routes'].append(self.gql_route)

        super().__init__(**kwargs)

    @property
    def gql_route(self) -> Route:

        return Route(
            path=self.gql_path,
            endpoint=self.gql_endpoint,
            methods=['POST'],
        )

    @cached_property
    def error_handlers_by_error(self) -> Dict[Type[Exception], ApixErrorHandler]:
        return {error_handler.error: error_handler for error_handler in self.error_handlers}

    def handle_error(self, error: Exception) -> ApixError:

        if isinstance(error, ApixError):
            return error

        error_handler = self.error_handlers_by_error.get(type(error))

        if error_handler:
            return error_handler.handle(error)

        else:
            return ApixError(
                message=error.args[0] if error.args else 'Something unexpected happened.',
                code='UNSPECIFIED',
            )

    async def gql_endpoint(self, request: Request) -> JSONResponse:

        context = ApixContext(
            request_id=uuid4(),
            requested_at=datetime.utcnow(),
        )

        auth_error = None
        if self.authenticator:
            token = request.headers.get('authorization', '')

            try:
                context.requested_by = await self.authenticator.authenticate(token)
            except Exception as error:
                auth_error = self.handle_error(error)

        query = await request.body()
        execution_result = await self.execute_query(query, context)

        if auth_error:
            if not execution_result.errors:
                execution_result.errors = []
            execution_result.errors.append(auth_error)

        if self.include_extensions:
            execution_result.extensions = context.extensions

        return JSONResponse(
            content=execution_result.formatted,
            status_code=200,
        )

    async def execute_query(
            self,
            query: bytes,
            context: ApixContext,
    ) -> ExecutionResult:

        body = json.loads(query)
        query = body.get('query', '')
        variables = body.get('variables', {})

        document_node = gql_parse(query)
        errors = gql_validate(self.gql_schema, document_node)

        if errors:
            for error in errors:
                error.extensions = {'code': 'SCHEMA_VIOLATION'}
            return ExecutionResult(errors=errors)

        execution_result = gql_execute(
            schema=self.gql_schema,
            document=document_node,
            context_value=context,
            variable_values=variables,
        )

        if inspect.isawaitable(execution_result):
            execution_result = await execution_result

        if execution_result.errors:
            for error in execution_result.errors:
                if not isinstance(error.original_error, ApixError):
                    error.extensions = {'code': 'SCHEMA_VIOLATION'}

        return execution_result

    @cached_property
    def query_resolvers(self) -> List[ApixQueryResolver]:
        return [resolver for resolver in self.resolvers if isinstance(resolver, ApixQueryResolver)]

    @cached_property
    def mutation_resolvers(self) -> List[ApixMutationResolver]:
        return [resolver for resolver in self.resolvers if isinstance(resolver, ApixMutationResolver)]

    @cached_property
    def gql_query_type(self) -> GraphQLObjectType | None:

        if self.query_resolvers:
            return GraphQLObjectType(
                name='Query',
                fields={resolver.field_name: resolver.gql_output_field for resolver in self.query_resolvers},
            )

    @cached_property
    def gql_mutation_type(self) -> GraphQLObjectType:

        if self.mutation_resolvers:
            return GraphQLObjectType(
                name='Mutation',
                fields={resolver.field_name: resolver.gql_output_field for resolver in self.mutation_resolvers},
            )

    @cached_property
    def gql_schema(self) -> GraphQLSchema:

        return GraphQLSchema(
            query=self.gql_query_type,
            mutation=self.gql_mutation_type,
            types=[GraphQLID, GraphQLString, GraphQLInt, GraphQLFloat, GraphQLBoolean, GraphQLDateTime]
        )
