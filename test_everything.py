import pytest
from app.models import*
from app.views import assign_quantities
import app.views as views

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
    sizes = ['S', 'M', 'L'] 

    size_percents = s.size_percents(sizes)
    assert len(size_percents) == 3
    assert abs(size_percents['S'] + size_percents['M'] + size_percents['L'] - 1) < .001

def test_size_percentage_with_sizes_that_dont_match():
    s = SizeCurve(**test_categories[2])
    sizes = ['xyz', '38948']
    sizes_expected = {size: None for size in sizes}
    assert s.size_percents(sizes) == sizes_expected

def test_size_with_high_sales_threshold():
    s = SizeCurve(**test_categories[2])
    sizes = ['S', 'M', 'L'] 
    assert s.size_percents(sizes, min_avg_sales_per_size=1000) !=  \
            s.size_percents(sizes, min_avg_sales_per_size=5)

def test_assigning_quantities():
    sizes = ['S', 'M', 'L'] 
    qty = 100
    quantities = assign_quantities(sizes=sizes, qty=qty, **test_categories[2])
    assert abs(sum([quantities[size] for size in sizes]) - 100) < 4

@pytest.mark.xfail
def test_quantities_assigned_sum_up_correctly():
    sizes = ['S', 'M', 'L'] 
    qty = 100
    quantities = assign_quantities(sizes=sizes, qty=qty, **test_categories[2])
    assert sum([quantities[size] for size in sizes]) == qty

