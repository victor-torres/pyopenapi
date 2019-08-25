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
        match, params, query = match_path('/pets', self.paths)
        self.assertEqual(match, '/pets')
        self.assertEqual(params, {})
        self.assertEqual(query, {})

    def test_query_path(self):
        match, params, query = match_path('/pets?limit=10', self.paths)
        self.assertEqual(match, '/pets')
        self.assertEqual(params, {})
        self.assertEqual(query, {'limit': '10'})

    def test_parameter_path(self):
        match, params, query = match_path('/pets/15', self.paths)
        self.assertEqual(match, '/pets/{pet_id}')
        self.assertEqual(params, {'pet_id': '15'})
        self.assertEqual(query, {})

    def test_not_found_path(self):
        with self.assertRaises(NotFoundError) as context:
            match_path('/petz', self.paths)

        self.assertEqual(context.exception.path, '/petz')


if __name__ == '__main__':
    unittest.main()
