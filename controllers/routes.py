# coding=utf-8
from controllers.medical_kit_instance import medical_kit_instance_blueprint, MedicalKitInstanceController
from controllers.service import service_blueprint, ServiceController
from controllers.medical import medical_blueprint, MedicalController


def init_app(current_app):
    # 服务
    service_blueprint.add_url_rule('/get_weixin_jsapi_params', 'get_weixin_jsapi_params_api', ServiceController.get_weixin_jsapi_params, methods=['get'])
    service_blueprint.add_url_rule('/download_weixin_media', 'download_weixin_media_api', ServiceController.download_weixin_media, methods=['get'])
    current_app.register_blueprint(service_blueprint, url_prefix='/api/service')
    # 药箱实例
    medical_kit_instance_blueprint.add_url_rule('/get', 'get_api', MedicalKitInstanceController.get, methods=['get'])
    medical_kit_instance_blueprint.add_url_rule('/set_setting', 'set_setting_api', MedicalKitInstanceController.set_setting, methods=['post'])
    current_app.register_blueprint(medical_kit_instance_blueprint, url_prefix='/api/medical_kit_instance')
    # 药品
    medical_blueprint.add_url_rule('/scan', 'scan_api', MedicalController.scan, methods=['get'])
    current_app.register_blueprint(medical_blueprint, url_prefix='/api/medical')
