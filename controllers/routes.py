# coding=utf-8
from controllers.medical_kit_instance import medical_kit_instance_blueprint, MedicalKitInstanceController
from controllers.service import service_blueprint, ServiceController
from controllers.medical import medical_blueprint, MedicalController


def init_app(current_app):
    # 服务
    service_blueprint.add_url_rule('/get_weixin_jsapi_params', 'get_weixin_jsapi_params_api', ServiceController.get_weixin_jsapi_params, methods=['get'])
    current_app.register_blueprint(service_blueprint, url_prefix='/api/service')
    # 管理员
    medical_kit_instance_blueprint.add_url_rule('/get', 'get_api', MedicalKitInstanceController.get, methods=['get'])
    current_app.register_blueprint(medical_kit_instance_blueprint, url_prefix='/api/medical_kit_instance')
    # 药品
    medical_blueprint.add_url_rule('/scan', 'scan_api', MedicalController.scan, methods=['get'])
    current_app.register_blueprint(medical_blueprint, url_prefix='/api/medical')
