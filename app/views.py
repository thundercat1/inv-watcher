from app import app
from models import *
import json
import requests

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
    sizes = request.args.get('sizes')
    style = request.args.get('style')

    if sizes is not None:
        sizes = sizes.split(',')

    if sizes is None and style is None:
        return 'Must include sizes argument if no style is provided', 400

    prod_group_id = request.args.get('pg')
    if prod_group_id is None and style is None:
        return 'Must include either pg or style', 400

    if style is not None:
        (prod_group_id, brand_name, sizes) = get_style_details(style)

    s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)
    return json.dumps(s.size_percents(sizes))


@app.route('/quantities', methods=['GET'])
def quantities():
    #Example calls:
    #http://localhost:5000/quantities?pg=100001246&brand=Columbia&sizes=M,L,XL
    #http://localhost:5000/quantities?style=COL3599&sizes=M,L,XL

    brand_name = request.args.get('brand')
    qty = int(request.args.get('qty'))
    style = request.args.get('style')

    if qty is None:
        return 'Must include qty argument', 400

    sizes = request.args.get('sizes')
    if sizes is not None:
        sizes = sizes.split(',')

    if sizes is None and style is None:
        return 'Must include sizes if no style is provided', 400

    prod_group_id = request.args.get('pg')
    style = request.args.get('style')
    if prod_group_id is None and style is None:
        return 'Must include either pg or style', 400

    if style is not None:
        (prod_group_id, brand_name, sizes) = get_style_details(style)

    s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)

    quantities = assign_quantities(sizes=sizes, qty=qty, brand_name=brand_name, prod_group_id=prod_group_id)

    print(quantities)

    return json.dumps(quantities)


def assign_quantities(sizes, qty, brand_name, prod_group_id):
    s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)
    size_percents = s.size_percents(sizes)
    return {size: int(qty*size_percents[size]) if size_percents[size] is not None else None for size in sizes}


def get_style_details(style):
    url = base_url + '/merchv3/products/%s' % (style)
    print(url)
    r = requests.get(url)
    if r.status_code != 200:
        print('Error retrieving PG from merch api')
        print(r.text)
        return None

    resp = json.loads(r.text)
    prod_group_id = resp['prodGroupId']
    brand_name = resp['brandName']

    sizes = set([])
    variants = resp['variants']
    [sizes.add(variant['axis2Value']) for variant in variants]

    return (prod_group_id, brand_name, sizes)


@app.route('/config', methods=['GET'])
def check_config():
    return 'Base URL: %s' % (base_url)

