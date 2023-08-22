from db import db


class AnimalTree(db.Model):
    __tablename__ = "animal_tree"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(120), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('animal_tree.id'))
    children = db.relationship('AnimalTree', cascade='all, delete-orphan',
                               backref=db.backref('parent', remote_side=[id]))

    def __init__(self, label, parent=None):
        self.label = label
        self.parent = parent

    def to_dict(self):
        children = [child.to_dict() for child in self.children]
        return {str(self.id): {'label': self.label, 'children': children}}


def seed_database():
    if len(AnimalTree.query.all()) == 0:
        root = AnimalTree('root')
        child1 = AnimalTree('Ant', parent=root)
        child2 = AnimalTree('Bear', parent=root)
        child3 = AnimalTree('Cat', parent=child2)
        child4 = AnimalTree('Dog', parent=child2)
        child5 = AnimalTree('Elephant', parent=child4)
        db.session.add_all([root, child1, child2, child3, child4, child5])
        db.session.commit()

        child6 = AnimalTree('Frog', parent=root)
        db.session.add(child6)
        db.session.commit()

