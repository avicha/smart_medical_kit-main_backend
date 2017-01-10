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
        file_path = env.STORAGE_FILE_DIR + '/weixin_media_'+media_id+'.amr'
        with open(file_path) as f:
            f.write(result)
        # 构建鉴权对象
        q = Auth(qiniu_config.access_key, qiniu_config.secret_key)
        # 要上传的空间
        bucket_name = 'weixin-media-resource'
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, media_id, 3600)
