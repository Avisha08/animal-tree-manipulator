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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, port=3001)
