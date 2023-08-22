Flask Animal Tree Service

This is a Flask RESTful API service that manages a hierarchical tree of animals. Sample tree will be saved in a sqlite database and SQLalchemy is used to communicate to the database.
The service provides endpoints to get and add nodes to the tree.


How to set up your service:
1. Clone this repository to your local machine.
2. cd to tree_service directory and set it as root
3. Ensure that python3 and pip are installed on your machine
4. Create a virtual environment for the project:
   `python -m venv env`
    
5. Activate the virtual environment:

    `source env/bin/activate`  # for Unix-like systems
    `env\Scripts\activate`  # for Windows
5.Install the required packages:
    `pip install -r requirements.txt`


How to run your service
To run the service, execute python app.py command in the root directory of the project. This will start a local development server on port 3001, and you can access the service by visiting http://localhost:3001/api/tree in your web browser or by making HTTP requests to the API endpoints.

Endpoints
The service provides the following endpoints:

GET /api/tree
This endpoint returns the entire tree as a JSON object. If the database is empty, it is seeded with initial data of a tree.

POST /api/tree
This endpoint adds a new node to the tree. The request body should be a JSON object with the following format:
{
    "parent": <parent_id>,
    "label": <label>
}
<parent_id> is the ID of the parent node to add the new node under, and <label> is the label of the new node. The endpoint returns a 201 Created status code if successful.

Design Choices:
The service uses Flask as the web framework and Flask-RESTful for creating RESTful APIs.
The hierarchical tree structure is represented using the adjacency list model in the AnimalTree model. Each node has a parent_id column that references the ID of its parent node, and a children relationship that is defined as a list of child nodes. This allows for easy traversal of the tree and querying for nodes with or without parents.
The to_dict() method in the AnimalTree model recursively generates a JSON object representing the node and its children.
The seed_database() function is used to seed the database with some sample data.
The JSON_SORT_KEYS configuration option is set to False to preserve the order of keys in the JSON response.