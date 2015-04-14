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
    #try prod_group_id = 22 and brand_name='Dynafit'
    def __init__(self, brand_name, prod_group_id):
        self.taxonomy = Taxonomy.query.filter_by(prod_group_id=prod_group_id).first().__dict__
        self.taxonomy.pop('_sa_instance_state', None)

    def get_taxonomy(self):
        return self.taxonomy

    def curve(self):
        query = Sales.query.filter_by(brand_name=brand_name, prod_group_name=self.taxonomy['prod_group_name'],
                merch_group_name=self.taxonomy['merch_group_name'], merch_div_name=self.taxonomy['merch_div_name'])
        return [{'size': result.size, 'quantity': result.quantity} for result in query.all()]
