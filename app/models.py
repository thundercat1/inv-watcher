from __future__ import print_function
from app import db
from sqlalchemy import func
from sqlalchemy.sql import label

class SalesBySize(db.Model):
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
        self.brand_name = brand_name

    def size_percents(self, sizes, min_avg_sales_per_size=20):
        if len(sizes) > 0:
            #First calculate matched sales at the PG
            pg_quantities = self.pg_quantities()
            matched_sales = {size: pg_quantities[size] for size in sizes if size in pg_quantities}
            sum_matched_sales = sum([matched_sales[size] for size in matched_sales])
            #print('Found', sum_matched_sales, 'sales at PG-Brand to use for size curve.')
        
        if sum_matched_sales < len(sizes)*min_avg_sales_per_size:
            #Not enough matches at PG - try going up to the Mg
            mg_quantities = self.mg_quantities()
            matched_sales = {size: mg_quantities[size] for size in sizes if size in mg_quantities}
            sum_matched_sales = sum([matched_sales[size] for size in matched_sales])
            #print('Found', sum_matched_sales, 'sales at MG-Brand to use for size curve.')

        if sum_matched_sales < len(sizes)*min_avg_sales_per_size:
            #Not enough matches at MG - go up to the MD
            md_quantities = self.md_quantities()
            matched_sales = {size: md_quantities[size] for size in sizes if size in md_quantities}
            sum_matched_sales = sum([matched_sales[size] for size in matched_sales])
            #print('Found', sum_matched_sales, 'sales at MD-Brand to use for size curve.')


        #print('Calculating size curve with the following sales data: ', matched_sales)
        return {size: matched_sales[size]/float(sum_matched_sales) if size in matched_sales else None 
                for size in sizes}


    def pg_quantities(self):
        #Filter to include sales with same brand, pg, mg, md
        sizes_query = db.session.query(SalesBySize.size, label('quantity', func.sum(SalesBySize.quantity))). \
            filter_by(brand_name=self.brand_name, prod_group_name=self.taxonomy['prod_group_name'],
                merch_group_name=self.taxonomy['merch_group_name'], merch_div_name=self.taxonomy['merch_div_name']).\
            group_by(SalesBySize.size)
        return {result.size: result.quantity for result in sizes_query.all()}


    def mg_quantities(self):
        #Filter to include sales with same brand, mg, md
        query = db.session.query(SalesBySize.size, label('quantity', func.sum(SalesBySize.quantity))). \
            filter_by(brand_name=self.brand_name, merch_group_name=self.taxonomy['merch_group_name'],
                      merch_div_name=self.taxonomy['merch_div_name']). \
            group_by(SalesBySize.size)
        return {result.size: result.quantity for result in query.all()}


    def md_quantities(self):
        #Filter to include sales with same brand, md
        query = db.session.query(SalesBySize.size, label('quantity', func.sum(SalesBySize.quantity))). \
            filter_by(brand_name=self.brand_name, merch_div_name=self.taxonomy['merch_div_name']). \
            group_by(SalesBySize.size)
        return {result.size: result.quantity for result in query.all()}
