from __future__ import print_function

from app import app
from app import cache
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

    ((prod_group_id, brand_name, sizes), error) = simplify_args(request)
    if error is not None:
        return error
    s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)
    return json.dumps(s.size_percents(sizes))

@app.route('/quantities', methods=['GET'])

def quantities():
    #Example calls:
    #http://localhost:5000/quantities?pg=100001246&brand=Columbia&sizes=M,L,XL
    #http://localhost:5000/quantities?style=COL3599&sizes=M,L,XL

    ((prod_group_id, brand_name, sizes), error) = simplify_args(request)
    if error is not None:
        return error

    qty = request.args.get('qty')
    try:
        qty = int(qty)
    except TypeError:
        return 'Must provide qty argument', 400

    s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)
    quantities = assign_quantities(sizes=sizes, qty=qty, brand_name=brand_name, prod_group_id=prod_group_id)
    print(quantities)
    return json.dumps(quantities)

def simplify_args(request):
    brand_name = request.args.get('brand')
    style = request.args.get('style')
    sizes = request.args.get('sizes')
    prod_group_id = request.args.get('pg')
    error = None

    if sizes is not None:
        sizes = sizes.split(',')

    if prod_group_id is None and style is None:
        error = ('Must include either pg or style', 400)
        return ((None,)*3, error)

    if sizes is None and style is None:
        error = ('Must include either a style or a list of sizes', 400)
        return ((None,)*3, error)

    if style is not None:
        style_details = get_style_details(style)
        print(style_details)
        print(style_details, error)
        return (style_details, error)

def assign_quantities(sizes, qty, brand_name, prod_group_id):
    s = SizeCurve(brand_name=brand_name, prod_group_id=prod_group_id)
    size_percents = s.size_percents(sizes)
    return {size: int(qty*size_percents[size]) if size_percents[size] is not None else None for size in sizes}

@cache.cached(timeout=60)
def get_style_details(style):
    url = base_url + '/merchv3/products/%s' % (style)
    print(url)
    r = requests.get(url)
    if r.status_code != 200:
        print('Error retrieving product data from merch api')
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

