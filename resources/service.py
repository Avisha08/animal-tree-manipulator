from flask import request
from flask_restful import Resource
from db import db
from models.animal_tree import AnimalTree


class TreeOperations(Resource):
    def get(self):
        root_nodes = AnimalTree.query.filter(AnimalTree.parent_id.is_(None)).all()
        tree = [node.to_dict() for node in root_nodes]
        return tree, 200

    def post(self):
        data = request.json

        if not data or data['parent'] is None or data['label'] is None:
            return {"status": False, "message": f"missing required fields"}, 400
        try:
            parent_id = int(data['parent'])
            label = data['label']
            parent = AnimalTree.query.filter_by(id=parent_id).first()
            if parent is None:
                return {"status": False, "message": f"parent does not exist"}, 404

            # TODO: check for duplicate node

            new_node = AnimalTree(label, parent=parent)
            db.session.add(new_node)
            db.session.commit()
        except Exception as e:
            return {"status": False, "message": f"Internal error"}, 500

        return {"status": True, "message": f"node added successfully"}, 201
