Database Design Choices
The AnimalTree model is designed as a self-referential table, where each row has a parent-child relationship with other rows in the table. This design allows for the creation of hierarchical tree structures, with each node having a label and an ID.

To achieve this, the model has four attributes:

id: the primary key of the table, which uniquely identifies each row.
label: a string that contains the name or label of each node.
parent_id: a foreign key that points to the parent of the current node. If the parent is null, then the current node is a root node.
children: a relationship that points to the children of the current node. It is a self-referential relationship that allows a node to have zero or more child nodes. 

The model also has two methods:

1. `__init__(self, label, parent=None)`: a constructor that takes in a label and an optional parent node and initializes the label and parent attributes of the current node.
2. `to_dict(self)`: a method that recursively converts the node and all its children to a dictionary.


Queries and Methods
The following are the queries and methods that can be used to interact with the AnimalTree database:

1. Adding a new node
   To add a new node to the AnimalTree database, the following steps can be taken:

   1. Create a new instance of the AnimalTree model, passing in the label and the parent node (if any).
   2. Add the new instance to the database session.
   3. Commit the changes to the database.
   Example:
       `parent = AnimalTree.query.filter_by(id=parent_id).first()
        new_node = AnimalTree(label, parent=parent)
        db.session.add(new_node)
        db.session.commit()`

2. Retrieving the root nodes
   To retrieve all the root nodes of the AnimalTree database, the following query can be used:

   `root_nodes = AnimalTree.query.filter(AnimalTree.parent_id.is_(None)).all()`
    This query returns all the nodes whose parent_id is null, which indicates that they are root nodes.
    
3. Retrieving a node and its children 
    Can be retrieved by following way using to_dict method:
    `root_nodes = AnimalTree.query.filter(AnimalTree.parent_id.is_(None)).all()
     tree = [node.to_dict() for node in root_nodes]`