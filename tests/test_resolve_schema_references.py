import unittest

from tests import load_yaml_fixture
from openapi.helpers import resolve_schema_references


class ResolveSchemaReferencesTestCase(unittest.TestCase):

    def test_should_resolve_schema_references(self):
        schema = load_yaml_fixture('petstore.yaml')
        expected_resolved_schema = load_yaml_fixture('resolved_petstore.yaml')
        resolved_schema = resolve_schema_references(schema)
        self.assertEqual(resolved_schema, expected_resolved_schema)

    def test_should_raise_exception_with_circular_references(self):
        schema = load_yaml_fixture('circular_reference_petstore.yaml')
        with self.assertRaises(RecursionError):
            resolve_schema_references(schema)


if __name__ == '__main__':
    unittest.main()
