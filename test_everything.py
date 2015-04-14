import pytest
from app.models import*

test_categories = [
    {'brand_name': 'Dynafit', 'prod_group_id': 22},
    {'brand_name': 'Park Tool', 'prod_group_id': 100000355},
    {'brand_name': 'Columbia', 'prod_group_id': 100001246},
    {'brand_name': 'Arc\'teryx', 'prod_group_id': 186}
]

def test_size_curve():
    s = SizeCurve(**test_categories[2])
    assert isinstance(s.taxonomy['merch_div_id'], int)
    assert isinstance(s.taxonomy['merch_group_name'], str)

    pg_sizes = s.pg_sizes()
    mg_sizes = s.mg_sizes()
    md_sizes = s.md_sizes()
    assert all([isinstance(pg_sizes[size], int) for size in pg_sizes.keys()])
    assert all([isinstance(mg_sizes[size], int) for size in mg_sizes.keys()])
    assert all([isinstance(md_sizes[size], int) for size in md_sizes.keys()])

    print('pg', pg_sizes)
    print('mg', mg_sizes)
    print('md', md_sizes)