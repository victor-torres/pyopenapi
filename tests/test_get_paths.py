import unittest

from openapi.helpers import get_paths

from tests import load_yaml_fixture


class GetPathsTestCase(unittest.TestCase):

    def test_get_paths(self):
        spec = load_yaml_fixture('petstore.yaml')
        paths = get_paths(spec)
        expected_paths = [
            '/pets',
            '/pets/{petId}'
        ]
        self.assertEqual(paths, expected_paths)

    def test_foo(self):
        from openapi import Request
        from openapi.helpers import validate_request
        spec = load_yaml_fixture('petstore.yaml')
        validate_request(spec, Request(url='/pets?limit=10', method='get', headers={}))


if __name__ == '__main__':
    unittest.main()
