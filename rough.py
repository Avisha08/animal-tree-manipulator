# this would print the tree in this format
# {
#   "1": {
#     "label": "root",
#     "children": {
#       "2": {
#         "label": "Ant"
#       },
#       "3": {
#         "label": "Bear",
#         "children": {
#           "5": {
#             "label": "Cat"
#           },
#           "6": {
#             "label": "Dog",
#             "children": {
#               "7": {
#                 "label": "Elephant"
#               }
#             }
#           }
#         }
#       },
#       "4": {
#         "label": "Frog"
#       }
#     }
#   }
# }


def get(self):
    seed_database()
    root_nodes = AnimalTree.query.filter(AnimalTree.parent_id.is_(None)).all()
    tree = [node.to_dict() for node in root_nodes]
    # print(tree)
    # print(json.dumps(tree))
    print(jsonify(tree))
    return jsonify(tree)


#OR

def get_tree():
    tree = {}
    roots = AnimalTree.query.filter_by(parent_id=None).all()
    for root in roots:
        tree[root.id] = build_tree(root)
    return jsonify(tree)


def build_tree(node):
    tree = {}
    tree['label'] = node.label
    children = node.children
    if children:
        tree['children'] = {}
        for child in children:
            tree['children'][child.id] = build_tree(child)
    return tree
