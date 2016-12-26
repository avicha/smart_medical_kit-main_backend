智能药箱——服务接口设计
== == == == ==

快速参考
--------
所有API调用均在/api/service命名空间下，访问域名，正式环境：http://smart_medical_kit.com，测试环境：http://dev.smart_medical_kit.com

URL|HTTP|功能
---|----|----
[/get_weixin_jsapi_params](#获取微信jsapi的配置参数)|GET|获取微信jsapi的配置参数

#### 获取微信jsapi的配置参数
向/get_weixin_jsapi_params发送GET请求，暂时url参数通过头部Referer获取：

获取成功，result返回以下字段：

字段|类型|意义
----|----|----
appId|string|公众号应用ID
nonceStr|string|随机字符串
signature|string|签名
timestamp|number|时间戳
