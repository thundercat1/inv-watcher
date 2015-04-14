import pytest
from app.models import*

def test_size_curve():
    s = SizeCurve("Dynafit", 22)
    assert s.taxonomy['merch_div_id'] == 12
    assert s.taxonomy['merch_group_name'] == 'Backcountry Boots'

    size_data = s.curve()
    assert all('quantity' in size for size in size_data)
    assert all('size' in size for size in size_data)