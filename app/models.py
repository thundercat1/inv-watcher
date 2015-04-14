from app import db

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_group_name = db.Column(db.String(128))
    merch_group_name = db.Column(db.String(128))
    merch_div_name = db.Column(db.String(128))
    brand_name = db.Column(db.String(128))
    quantity = db.Column(db.Integer)
    size = db.Column(db.String(128))


class Taxonomy(db.Model):
    prod_group_id = db.Column(db.Integer, primary_key=True)
    merch_group_id = db.Column(db.Integer)
    merch_div_id = db.Column(db.Integer)
    prod_group_name = db.Column(db.String(128))
    merch_group_name = db.Column(db.String(128))
    merch_div_name = db.Column(db.String(128))


class SizeCurve():
    #try prod_group_id = 17 and brand_name='Dynafit'
    
    def __init__(self, brand_name, prod_group_name):
        self.query = Sales.query.filter_by(brand_name=brand_name, prod_group_name=prod_group_name)

    def curve(self):
        return [{'size': result.size, 'quantity': result.quantity} for result in self.query.all()]
    
