# coding=utf-8


def test_get_weixin_jsapi_params(api_get):
    errcode, result = api_get('/api/service/get_weixin_jsapi_params', headers={'Referer': 'http://smart_medical_kit.com'})
    assert errcode == 0
    assert 'appId' in result
    assert 'nonceStr' in result
    assert 'signature' in result
    assert 'timestamp' in result
