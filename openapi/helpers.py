import re
import typing
import urllib.parse

import jsonschema


from openapi import (
    Request,
)
from openapi.exceptions import (
    ValidationError,
    NotFoundError,
    MethodNotAllowed,
)


def resolve_schema_references(schema: dict, base_uri: str = None) -> dict:
    """This function resolves references in a JSON Schema dict.

    This function may raise a RecursionError exception if one or more JSON
    Schemas provided as a parameter or found by the JSON Schema Reference
    Resolver contains circular references.

    :param schema: a JSON Schema dict with unresolved references
    :param base_uri: optional path to search for additional JSON Schema files
    :return: a JSON Schema dict with resolved references
    """
    resolver = jsonschema.RefResolver(base_uri or '', schema)

    def _resolve_schema_references(_schema):
        if not isinstance(_schema, dict):
            return _schema

        if '$ref' in _schema.keys():
            _, resolved_schema = resolver.resolve(_schema['$ref'])
            return _resolve_schema_references(resolved_schema)

        return {k: _resolve_schema_references(v) for k, v in _schema.items()}

    return _resolve_schema_references(schema)


def validate_schema(schema: dict, content: typing.Any) -> None:
    """This function validates content against a JSON Schema.

    If there are validation errors, an openapi.exceptions.ValidationError
    exception is raised. Take a look at its definition for more details.

    :param schema: a JSON Schema dict
    :param content: anything to be validated against the JSON Schema
    :return: None
    """
    validator = jsonschema.Draft4Validator(schema)

    try:
        validator.validate(content)
    except jsonschema.ValidationError:
        errors = [e.message for e in validator.iter_errors(content)]
        raise ValidationError(errors)


def match_path(url: str, paths: typing.List[str]) -> typing.Tuple[str, dict]:
    """This function matches an URL and its parameters against a list of
    OpenAPI paths.

    :param url: a string with an URL (e.g.: /pets, /pets?limit=10 or /pets/15)
    :param paths: a list of OpenAPI path strings (e.g.: /pets, /pets/{pet_id})
    :return: a tuple with the OpenAPI path, its path and query parameters dicts
    """
    _url = urllib.parse.urlsplit(url)
    for candidate in paths:
        path_regex = re.sub(r'\{(\w+)\}', r'(?P<\1>\\w+)', f'^{candidate}$')
        match = re.match(path_regex, _url.path)
        if not match:
            continue

        path_params = match.groupdict()
        query_params = dict(urllib.parse.parse_qsl(_url.query))
        return candidate, path_params, query_params

    raise NotFoundError(_url.path)


def get_paths(spec: dict) -> typing.List[str]:
    """This function extracts a list of paths from an OpenAPI specification.

    :param spec: a dict with an OpenAPI specification
    :return: a list of OpenAPI path strings (e.g.: /pets, /pets/{pet_id})
    """
    return [str(k) for k in spec['paths'].keys()]


def validate_request(spec: dict, request: Request) -> None:
    """This function validates path parameters against an OpenAPI specification.

    :param spec: a dict with an OpenAPI specification
    :param path: an OpenAPI path strings (e.g.: /pets, /pets/{pet_id})
    :param params: a dictionary with path parameters (e.g.: {'limit': '10'})
    :return: None
    """
    path, path_params, query_params = match_path(request.url, get_paths(spec))

    try:
        method_spec = spec['paths'][path][request.method]
    except KeyError:
        raise MethodNotAllowed(path, request.method)

    errors = []
    for param in method_spec.get('parameters', []):
        _type = param['in']
        name = param['name']
        required = param.get('required', False)

        if _type == 'path':
            if name not in path_params and required:
                errors.append(f'Path parameter {name} is required')
                continue

            value = path_params.get(name)

        elif _type == 'query':
            if name not in query_params and required:
                errors.append(f'Query parameter {name} is required')
                continue

            value = query_params.get(name)

        else:
            raise NotImplementedError(f'Parameter type {_type} not supported')

        if param['schema']['type'] == 'integer':
            try:
                value = int(value)
            except TypeError:
                pass

        try:
            validate_schema(param['schema'], value)
        except ValidationError as exc:
            errors += exc.errors

    if errors:
        raise ValidationError(errors)
