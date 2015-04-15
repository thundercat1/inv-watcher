import pytest
from app.models import*

test_categories = [
    {'brand_name': 'Dynafit', 'prod_group_id': 22},
    {'brand_name': 'Park Tool', 'prod_group_id': 100000355},
    {'brand_name': 'Columbia', 'prod_group_id': 100001246},
    {'brand_name': 'Arc\'teryx', 'prod_group_id': 186}
]

def test_size_curve():
    for test in test_categories:
        print('Testing', test['brand_name'], 'prod group', test['prod_group_id'])
        s = SizeCurve(**test)
        assert isinstance(s.taxonomy['merch_div_id'], int)
        assert isinstance(s.taxonomy['merch_group_name'], (unicode, str))

        pg_quantities = s.pg_quantities()
        mg_quantities = s.mg_quantities()
        md_quantities = s.md_quantities()
        assert all([isinstance(pg_quantities[size], int) for size in pg_quantities.keys()])
        assert all([isinstance(mg_quantities[size], int) for size in mg_quantities.keys()])
        assert all([isinstance(md_quantities[size], int) for size in md_quantities.keys()])

        print(pg_quantities)

def test_calculating_size_curve_percentages():
    #first test with columbia
    s = SizeCurve(**test_categories[2])
    sizes = {'S': None, 'M': None, 'L': None}

    size_percents = s.size_percents(sizes)
    print(size_percents)
    assert len(size_percents) == 3
    assert abs(size_percents['S'] + size_percents['M'] + size_percents['L'] - 1) < .001


