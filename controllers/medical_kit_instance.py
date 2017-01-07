# coding=utf-8
from flask import Blueprint

from backend_common.controllers.medical_kit_instance import MedicalKitInstanceController as MedicalKitInstanceCommonController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.medical_kit import MedicalKit as MedicalKitModel
from backend_common.models.medical_kit_instance import MedicalKitInstance as MedicalKitInstanceModel

medical_kit_instance_blueprint = Blueprint('medical_kit_instance', __name__)


class MedicalKitInstanceController(MedicalKitInstanceCommonController):

    @classmethod
    @get_request_params()
    def get(cls, data):
        medical_kit_instance_id = data.get('medical_kit_instance_id')
        medical_kit_instance_model = MedicalKitInstanceModel(id=medical_kit_instance_id)
        medical_kit_instance = MedicalKitInstanceModel.select(MedicalKitInstanceModel.id, MedicalKitModel.product_code, MedicalKitModel.name, MedicalKitModel.image, MedicalKitModel.box_count).join(MedicalKitModel, on=(MedicalKitInstanceModel.product_code == MedicalKitModel.product_code)).where(MedicalKitInstanceModel.id == medical_kit_instance_id).dicts().first()
        if medical_kit_instance:
            setting = medical_kit_instance_model.setting()
            box_settings = medical_kit_instance_model.box_settings(medical_kit_instance.get('box_count'))
            medical_kit_instance.update({'setting': setting, 'box_settings': box_settings})
            return cls.success_with_result(medical_kit_instance)
        else:
            raise MedicalKitInstanceModel.NotFoundError('找不到该药箱')
