智能药箱——药箱实例接口设计
==========

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
setting|object|药箱设置
setting.id|number|药箱设置ID
setting.prompt_sound|string|药箱提示音
box_settings|array|药箱盒子设置
box_settings[0].id|number|药箱盒子设置ID
box_settings[0].box_index|number|设置第几个药箱盒子
box_settings[0].medical_name|string|药箱盒子药物名称
box_settings[0].medical_barcode|string|药箱盒子药物条形码
box_settings[0].schedule_times|string|药箱盒子吃药时间，用逗号分隔
box_settings[0].piece_per_time|number|药箱盒子每次吃药分量
box_settings[0].unit|string|药箱盒子药物单位
