# coding=utf-8
from flask import Blueprint

from backend_common.controllers.medical_kit_instance_setting import MedicalKitInstanceSettingController as MedicalKitInstanceSettingCommonController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.medical_kit_instance_setting import MedicalKitInstanceSetting as MedicalKitInstanceSettingModel
from backend_common.models.medical_kit_instance_box_setting import MedicalKitInstanceBoxSetting as MedicalKitInstanceBoxSettingModel

medical_kit_instance_setting_blueprint = Blueprint('medical_kit_instance_setting', __name__)


class MedicalKitInstanceSettingController(MedicalKitInstanceSettingCommonController):

    @classmethod
    @get_request_params()
    def create(cls, data):
        medical_kit_instance_id = data.get('medical_kit_instance_id')
        medical_kit_instance = MedicalKitInstanceModel.select(MedicalKitInstanceModel.id, MedicalKitModel.product_code, MedicalKitModel.name, MedicalKitModel.image, MedicalKitModel.box_count).join(MedicalKitModel, on=(MedicalKitInstanceModel.product_code == MedicalKitModel.product_code)).dicts().first()
        if medical_kit_instance:
            return cls.success_with_result(medical_kit_instance)
        else:
            raise MedicalKitInstanceModel.NotFoundError('找不到该药箱')
