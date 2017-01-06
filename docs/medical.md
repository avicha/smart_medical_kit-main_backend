智能药箱——药品接口设计
== == == == ==

快速参考
--------
所有API调用均在/api/medical命名空间下，访问域名，正式环境：http://smart_medical_kit.com，测试环境：http://dev.smart_medical_kit.com

URL|HTTP|功能
---|----|----
[/scan](#扫描条形码)|GET|扫描条形码

#### 扫描条形码
向/scan发送GET请求，请求参数如下：

字段|类型|意义
----|----|----
barcode|string|条形码

获取成功，result返回以下字段：

字段|类型|意义
----|----|----
name|string|药品名称
barcode|string|药品条形码
amount_desc|string|药品用量描述
