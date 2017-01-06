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
        assert 'setting' in result
        assert 'box_settings' in result
        setting = result.get('setting')
        box_settings = result.get('box_settings')
        if setting:
            assert 'id' in setting
            assert 'prompt_sound' in setting
        if len(box_settings) > 0:
            box_setting = box_settings[0]
            assert 'id' in box_setting
            assert 'box_index' in box_setting
            assert 'medical_name' in box_setting
            assert 'medical_barcode' in box_setting
            assert 'schedule_times' in box_setting
            assert 'piece_per_time' in box_setting
            assert 'unit' in box_setting
