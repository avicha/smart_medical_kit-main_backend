# coding=utf-8
from controllers.medical_kit_instance import medical_kit_instance_blueprint, MedicalKitInstanceController


def init_app(current_app):
    # 管理员
    medical_kit_instance_blueprint.add_url_rule('/get', 'get_api', MedicalKitInstanceController.get, methods=['get'])
    current_app.register_blueprint(medical_kit_instance_blueprint, url_prefix='/api/medical_kit_instance')
