from flask import Flask
from flask_restful import Api
from db import db
import models
from models.animal_tree import seed_database
from resources.service import TreeOperations


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animal_tree.db'
app.config['JSON_SORT_KEYS'] = False
db.init_app(app)

api = Api(app)

api.add_resource(TreeOperations, '/api/tree')




# class AnimalTree(db.Model):
#     __tablename__ = "animal_tree"
#
#     id = db.Column(db.Integer, primary_key=True)
#     label = db.Column(db.String(120), nullable=False)
#     parent_id = db.Column(db.Integer, db.ForeignKey('animal_tree.id'))
#     children = db.relationship('AnimalTree', cascade='all, delete-orphan',
#                                backref=db.backref('parent', remote_side=[id]))
#
#     def __init__(self, label, parent=None):
#         self.label = label
#         self.parent = parent
#
#     def to_dict(self):
#         children = [child.to_dict() for child in self.children]
#         return {str(self.id): {'label': self.label, 'children': children}}
#
#
# def seed_database():
#     if len(AnimalTree.query.all()) == 0:
#         root1 = AnimalTree('Mammals')
#         root2 = AnimalTree('Birds')
#         child1 = AnimalTree('Cats', parent=root1)
#         child2 = AnimalTree('Dogs', parent=root1)
#         child3 = AnimalTree('Canaries', parent=root2)
#         db.session.add_all([root1, root2, child1, child2, child3])
#         db.session.commit()
#
#
# class TreeOperations(Resource):
#     def get(self):
#         seed_database()
#         root_nodes = AnimalTree.query.filter(AnimalTree.parent_id.is_(None)).all()
#         tree = [node.to_dict() for node in root_nodes]
#         return jsonify(tree)
#
#     def post(self):
#         data = request.get_json()
#         parent_id = int(data['parent'])
#         label = data['label']
#         parent = AnimalTree.query.filter_by(id=parent_id).first()
#         new_node = AnimalTree(label, parent=parent)
#         db.session.add(new_node)
#         db.session.commit()
#         return '', 201
#
#
# api.add_resource(TreeOperations, '/api/tree')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, port=3001)




# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resource, Api
# from flasgger import Swagger
# import os
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animal_tree.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# swagger = Swagger(app)
#
#
# class TreeNode(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     label = db.Column(db.String(50), nullable=False)
#     parent_id = db.Column(db.Integer, db.ForeignKey('tree_node.id'))
#     children = db.relationship('TreeNode')
#
#     def to_dict(self):
#         children = []
#         for child in self.children:
#             children.append(child.to_dict())
#         return {
#             str(self.id): {
#                 'label': self.label,
#                 'children': children
#             }
#         }
#
#     def add_child(self, label):
#         child = TreeNode(label=label, parent_id=self.id)
#         db.session.add(child)
#         db.session.commit()
#         return child.id
#
#
# def seed_database():
#     # Seed the database with a sample tree if it's empty
#     if len(TreeNode.query.all()) == 0:
#         print("seeding db")
#         root = TreeNode(label='Animal')
#         db.session.add(root)
#
#         cat_id = root.add_child('Cat')
#         dog_id = root.add_child('Dog')
#
#         cat = TreeNode.query.filter_by(cat_id)
#         cat.add_child('Lion')
#         cat.add_child('Tiger')
#
#         dog = TreeNode.query.filter_by(dog_id)
#         dog.add_child('Golden Retriever')
#         dog.add_child('Labrador Retriever')
#
#         db.session.commit()
#
#
# @app.route('/', methods=['GET'])
# def home():
#     # Get the root node and return the entire tree
#     return "I'm Home"
#
#
# @app.route('/api/tree', methods=['GET'])
# def get_tree():
#     # Get the root node and return the entire tree
#     root = TreeNode.query.filter_by(parent_id=None).first()
#     return jsonify(root.to_dict())
#
#
# @app.route('/api/tree', methods=['POST'])
# def add_node():
#     parent_id = request.json['parent']
#     label = request.json['label']
#     parent = TreeNode.query.get(parent_id)
#     node_id = parent.add_child(label)
#     return jsonify({'id': node_id})
#
#
# if __name__ == '__main__':
#     # Seed the database with a sample tree if it's empty
#     with app.app_context():
#         db.create_all()
#         seed_database()
#     # Start the Flask app
#     app.run(port=3001)
