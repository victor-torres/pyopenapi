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


if __name__ == '__main__':
    unittest.main()
