from app import app
from models import *
import json

from flask import request
from config import base_url

@app.route('/')
def root():
    return('hello')

@app.route('/sizeCurves', methods=['GET'])
def sizeCurves():
    #Example calls:
    #http://localhost:5000/sizeCurves?pg=100001246&brand=Columbia&sizes=M,L,XL
    #http://localhost:5000/sizeCurves?style=COL3599&brand=Columbia&sizes=M,L,XL

    brand_name = request.args.get('brand')
    sizes = request.args.get('sizes').split(',')

    if brand_name is None or sizes is None:
        return 'Must include both brand and size arguments', 400

    prod_group_id = request.args.get('pg')
    if prod_group_id is not None:
        s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)
        return json.dumps(s.size_percents(sizes))

    else:
        style = request.args.get('style')
        if style is None:
            return 'Error: You must include either pg or style argumet', 400


@app.route('/quantities/pg', methods=['GET'])
def quantitiesByPg():
    brand_name = request.args.get('brand')
    prod_group_id = request.args.get('pg')
    sizes = request.args.get('sizes').split(',')
    qty = request.args.get('qty')

    return json.dumps(assign_quantities(sizes=sizes, qty=qty, 
        brand_name=brand_name, prod_group_id=prod_group_id))


def assign_quantities(sizes, qty, brand_name, prod_group_id):
    s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)
    size_percents = s.size_percents(sizes)
    return {size: int(qty*size_percents[size]) for size in sizes}

@app.route('/config', methods=['GET'])
def check_config():
    return 'Base URL: %s' % (base_url)
