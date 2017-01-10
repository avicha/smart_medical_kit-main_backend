# coding=utf-8
from flask import Blueprint

from backend_common.controllers.service import ServiceController as ServiceCommonController
from backend_common.middlewares.request_service import get_request_params
import env

service_blueprint = Blueprint('service', __name__)

from backend_common.services.weixin_api import WeixinAPI
from backend_common.config import weixin as weixin_api_config
weixin_api = WeixinAPI(weixin_api_config)

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from backend_common.config import qiniu as qiniu_config


class ServiceController(ServiceCommonController):

    @classmethod
    @get_request_params()
    def download_weixin_media(cls, data):
        media_id = data.get('media_id')
        result = weixin_api.get_media(media_id)
        localfile = env.STORAGE_FILE_DIR + '/weixin_media_'+media_id+'.amr'

        with open(localfile, 'w') as f:
            f.write(result)
        # 要上传的空间
        bucket_name = 'weixin-media-resource'
        key = media_id+'.amr'
        # 设置转码参数
        fops = 'avthumb/amr/acodec/mp3'
        # 转码时使用的队列名称
        pipeline = 'weixin_media'
        # 构建鉴权对象
        q = Auth(qiniu_config.access_key, qiniu_config.secret_key)
        # 可以对转码后的文件进行使用saveas参数自定义命名，当然也可以不指定文件会默认命名并保存在当前空间
        saveas_key = urlsafe_base64_encode(bucket_name+':'+media_id+'.mp3')
        fops = fops+'|saveas/'+saveas_key
        # 在上传策略中指定
        policy = {
            'persistentOps': fops,
            'persistentPipeline': pipeline
        }
        # 生成上传Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600, policy)
        ret, info = put_file(token, key, localfile)
        print ret, info
        return cls.success_with_result('http://'+qiniu_config.resource_domain+'/'+ret['key'])
