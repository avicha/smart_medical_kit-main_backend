智能药箱——药箱实例接口设计
== == == == ==

快速参考
--------
所有API调用均在/api/medical_kit_instance命名空间下，访问域名，正式环境：http://smart_medical_kit.com，测试环境：http://dev.smart_medical_kit.com

URL|HTTP|功能
---|----|----
[/get](#获取)|GET|获取

#### 获取
向/get发送GET请求，请求参数如下：

字段|类型|意义
----|----|----
medical_kit_instance_id|number|药箱实例ID

获取成功，result返回以下字段：

字段|类型|意义
----|----|----
id|number|药箱实例ID
product_code|number|产品编码
name|string|药箱名称
image|string|药箱图片
box_count|number|药箱格子数
