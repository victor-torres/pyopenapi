import unittest

from openapi.helpers import match_path
from openapi.exceptions import NotFoundError


class MatchPathTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.paths = (
            '/pets',
            '/pets/{pet_id}',
        )

    def test_simple_path(self):
        path_match, path_parameters = match_path('/pets', self.paths)
        self.assertEqual(path_match, '/pets')
        self.assertEqual(path_parameters, {})

    def test_parameter_path(self):
        path_match, path_parameters = match_path('/pets/15', self.paths)
        self.assertEqual(path_match, '/pets/{pet_id}')
        self.assertEqual(path_parameters, {'pet_id': '15'})

    def test_not_found_path(self):
        with self.assertRaises(NotFoundError) as context:
            match_path('/petz', self.paths)

        self.assertEqual(context.exception.path, '/petz')


if __name__ == '__main__':
    unittest.main()
