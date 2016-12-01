智能药箱——用户接口设计
==========

快速参考
--------
所有API调用均在/api/user命名空间下，访问域名，正式环境：http://smart_medical_kit.com，测试环境：http://dev.smart_medical_kit.com

URL|HTTP|功能
---|----|----
[/register](#注册)|POST|注册
[/login](#登录)|POST|登录
[/logout](#退出登录)|GET|退出登录
[/reset_password](#重置密码)|POST|重置密码
[/current](#获取当前用户)|GET|获取当前用户
[/update](#更新用户信息)|POST|更新用户信息

#### 注册
向/register发送POST请求，请求参数如下：

字段|类型|意义
----|----|----
phone_number|string|手机号码
password|string|密码
verifycode|string|6位验证码

注册成功result返回用户ID和自动登录的token：

字段|类型|意义
----|----|----
id|number|用户ID
username|string|用户名
sex|number|性别
phone_number|string|手机号码
nick|string|昵称
avatar|string|头像URL
register_type|number|注册类型
created_at|date|注册时间
token|string|令牌token

#### 登录
向/login发送POST请求，请求参数如下：

字段|类型|意义
----|----|----
username|string|用户名
password|string|密码

登录成功result返回用户信息：

字段|类型|意义
----|----|----
id|number|用户ID
username|string|用户名
sex|number|性别
phone_number|string|手机号码
nick|string|昵称
avatar|string|头像URL
register_type|number|注册类型
created_at|date|注册时间
token|string|令牌token

#### 退出登录
向/logout发送GET请求，请求参数如下：

字段|类型|意义
----|----|----
token|string|令牌token

成功退出登录result返回更新时间：

字段|类型|意义
----|----|----
updated_at|date|上次修改时间

#### 重置密码
向/reset_password发送POST请求，请求参数如下：

字段|类型|意义
----|----|----
old_password|string|旧密码
new_password|string|新密码
token|string|令牌token

成功修改则返回errcode=0错误码

#### 获取当前用户
向/current发送GET请求，请求参数如下：

字段|类型|意义
----|----|----
token|string|令牌token，如果有的话

当前用户已经失效或不存在则返回None，否则返回用户当前信息：

字段|类型|意义
----|----|----
id|number|用户ID
username|string|用户名
sex|number|性别
phone_number|string|手机号码
nick|string|昵称
avatar|string|头像URL
register_type|number|注册类型
created_at|date|注册时间

#### 更新用户信息
向/update发送POST请求，请求参数如下：

字段|类型|意义
----|----|----
sex|number|性别
nick|string|昵称
avatar|string|头像
token|string|令牌token

修改成功返回更新时间：

字段|类型|意义
----|----|----
updated_at|date|更新时间
