# import unittest
# import json
# from app import app
# from db import db
# from models import AnimalTree
#
#
# class TreeOperationsTestCase(unittest.TestCase):
#     def setUp(self):
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_animal_tree.db'
#         app.config['TESTING'] = True
#         self.app = app.test_client()
#         db.create_all()
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#
#     def test_get_tree(self):
#         response = self.app.get('/api/tree')
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(len(data), 2)
#         self.assertEqual(data[0]['1']['label'], 'Mammals')
#         self.assertEqual(data[1]['2']['label'], 'Birds')
#
#     def test_add_node(self):
#         parent = AnimalTree('Mammals')
#         db.session.add(parent)
#         db.session.commit()
#
#         new_node_data = {'label': 'Cats', 'parent': parent.id}
#         response = self.app.post('/api/tree', json=new_node_data)
#         self.assertEqual(response.status_code, 201)
#
#         # Check if the new node was added to the database
#         nodes = AnimalTree.query.all()
#         self.assertEqual(len(nodes), 2)
#         self.assertEqual(nodes[1].label, 'Cats')
#         self.assertEqual(nodes[1].parent, parent)
#
#     def test_add_node_invalid_parent(self):
#         new_node_data = {'label': 'Cats', 'parent': 999}
#         response = self.app.post('/api/tree', json=new_node_data)
#         self.assertEqual(response.status_code, 400)
#         data = json.loads(response.data)
#         self.assertEqual(data['message'], 'Invalid parent node id')
#
#     def test_add_node_duplicate(self):
#         parent = AnimalTree('Mammals')
#         child1 = AnimalTree('Cats', parent=parent)
#         db.session.add_all([parent, child1])
#         db.session.commit()
#
#         new_node_data = {'label': 'Cats', 'parent': parent.id}
#         response = self.app.post('/api/tree', json=new_node_data)
#         self.assertEqual(response.status_code, 400)
#         data = json.loads(response.data)
#         self.assertEqual(data['message'], 'Node already exists')


import unittest
import json
from flask import Response
from app import app
from db import db
from models.animal_tree import AnimalTree, seed_database


# class TestTreeOperations(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Set up the test database
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         app.config['TESTING'] = True
#         with app.app_context():
#             # db.init_app(app)
#             db.create_all()
#             seed_database()
#
#     @classmethod
#     def tearDownClass(cls):
#         # Clean up the test database
#         with app.app_context():
#             db.session.remove()
#             db.drop_all()
#
#     def setUp(self):
#         # Set up a test client and push a new application context
#         self.app = app.test_client()
#         self.ctx = app.app_context()
#         self.ctx.push()
#
#     def tearDown(self):
#         # Pop the application context
#         self.ctx.pop()
#
#     def test_get(self):
#         response = self.app.get('/api/tree')
#         data = jsonify(response.get_json())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(data), 2)
#
#     def test_post(self):
#         # Test adding a new node to the tree
#         data = {'parent': '1', 'label': 'Elephants'}
#         response = self.app.post('/api/tree', json=data)
#         self.assertEqual(response.status_code, 201)
#         node = AnimalTree.query.filter_by(label='Elephants').first()
#         self.assertIsNotNone(node)
#         self.assertEqual(node.parent.label, 'Mammals')
#
#         # Test adding a duplicate node to the tree
#         data = {'parent': '1', 'label': 'Dogs'}
#         response = self.app.post('/api/tree', json=data)
#         self.assertEqual(response.status_code, 409)
#         node = AnimalTree.query.filter_by(label='Dogs').all()
#         self.assertEqual(len(node), 1)
#         self.assertEqual(node[0].parent.label, 'Mammals')
#




class TestTree(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            self.client = app.test_client()
            db.create_all()
            seed_database()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get(self):
        response = self.client.get('/api/tree')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)

    def test_post(self):
        with app.app_context():
            client = app.test_client()
            response = client.post('/api/tree', json={"parent": 1, "label": "Hen"})
            self.assertEqual(response.status_code, 201)
            node = AnimalTree.query.filter_by(label="Hen").first()
            self.assertIsNotNone(node)
            self.assertEqual(node.parent.label, 'root')

    def test_post_duplicate(self):
        response = self.client.post('/api/tree', json={"parent": 1, "label": "Hen"})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/tree', json={"parent": 1, "label": "Hen"})
        self.assertEqual(response.status_code, 400)

