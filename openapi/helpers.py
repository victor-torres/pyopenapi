import re
import typing

import jsonschema


from openapi.exceptions import (
    ValidationError,
    NotFoundError,
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


def match_path(path: str, paths: typing.List[str]) -> typing.Tuple[str, dict]:
    """This function matches a path and its parameters against a list of
    OpenAPI paths.

    :param path: a string with a formatted path (e.g.: /pets or /pets/15)
    :param paths: a list of OpenAPI path strings (e.g.: /pets, /pets/{pet_id})
    :return: a tuple with the OpenAPI path and its parameters dict
    """
    for candidate in paths:
        path_regex = re.sub(r'\{(\w+)\}', r'(?P<\1>\\w+)', f'^{candidate}$')
        match = re.match(path_regex, path)
        if not match:
            continue

        return candidate, match.groupdict()

    raise NotFoundError(path)


def get_paths(spec: dict) -> typing.List[str]:
    """This function extracts a list of paths from an OpenAPI specification.

    :param spec: a dict with an OpenAPI specification
    :return: a list of OpenAPI path strings (e.g.: /pets, /pets/{pet_id})
    """
    return [str(k) for k in spec['paths'].keys()]
