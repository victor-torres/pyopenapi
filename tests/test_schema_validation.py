import unittest

from openapi.helpers import validate_schema
from openapi.exceptions import ValidationError


class SchemaValidationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.schema = {
            'type': 'string',
            'pattern': '^my string$',
        }

    def test_valid_schema_validation(self):
        self.assertIsNone(validate_schema(self.schema, 'my string'))

    def test_invalid_schema_validation(self):
        with self.assertRaises(ValidationError):
            validate_schema(self.schema, '')


if __name__ == '__main__':
    unittest.main()
