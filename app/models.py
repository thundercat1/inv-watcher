from app import db

class SpaceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    def __init__(self, type):
        self.type = type


class Space(db.Model):
    location = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), db.ForeignKey('space_type.type'))
    name = db.Column(db.String(64))

class Property(Space):
    price = db.Column(db.Integer)
    color_group = db.Column(db.String(64))

    def __init__(self, name, price, color_group, location):
        self.location = location;
        self.type = 'Property'
        self.name = name
        self.price = price
        self.color_group = color_group

class Tax(Space):
    amount = db.Column(db.Integer)
    
    def __init__(self, name, location):
        self.type = 'Tax'
        self.name = name
        self.location = location
