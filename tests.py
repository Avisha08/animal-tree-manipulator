import unittest
import json
from app import app
from db import db
from resources.service import TreeOperations


class TestAnimalTree(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        # TreeOperations.seed_database()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_root_nodes(self):
        response = self.app.get('/api/tree')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertIn('Mammals', data[0]['1']['label'])
        self.assertIn('Birds', data[1]['2']['label'])

    def test_add_node(self):
        data = {'parent': 1, 'label': 'Elephants'}
        response = self.app.post('/api/tree', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Elephants', response.data.decode())
        self.assertIn('Cats', response.data.decode())

    def test_add_node_to_nonexistent_parent(self):
        data = {'parent': 100, 'label': 'Elephants'}
        response = self.app.post('/api/tree', json=data)
        self.assertEqual(response.status_code, 404)

    def test_add_duplicate_node(self):
        data = {'parent': 1, 'label': 'Cats'}
        response = self.app.post('/api/tree', json=data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

