# coding=utf-8


def test_medical_kit_instance_get(api_get, medical_kit_instance):
    if medical_kit_instance:
        errcode, result = api_get('/api/medical_kit_instance/get', data={'medical_kit_instance_id': medical_kit_instance.id})
        assert errcode == 0
        assert 'id' in result
        assert 'product_code' in result
        assert 'name' in result
        assert 'image' in result
        assert 'box_count' in result
