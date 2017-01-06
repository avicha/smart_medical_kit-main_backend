# coding=utf-8


def test_medical_scan(api_get):
    errcode, result = api_get('/api/medical/scan', data={'barcode': '6953460846432'})
    assert errcode == 0
    assert 'name' in result
    assert 'barcode' in result
    assert 'amount_desc' in result
