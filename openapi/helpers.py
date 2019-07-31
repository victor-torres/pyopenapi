import jsonschema


def resolve_schema_references(schema: dict, base_uri: str = None) -> dict:
    """This function resolves references in a JSON Schema dict.

    This function may raise a RecursionError exception if one or more JSON
    Schemas provided as a parameter or found by the JSON Schema Reference
    Resolver contains circular references.

    :param schema: a JSON Schema dict with unresolved references.
    :param base_uri: optional path to search for additional JSON Schema files.
    :return: a JSON Schema dict with resolved references.
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
