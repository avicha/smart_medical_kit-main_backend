# coding=utf-8
from flask import Blueprint

from backend_common.controllers.medical_kit_instance import MedicalKitInstanceController as MedicalKitInstanceCommonController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.medical_kit import MedicalKit as MedicalKitModel
from backend_common.models.medical_kit_instance import MedicalKitInstance as MedicalKitInstanceModel
from backend_common.models.medical_kit_instance_setting import MedicalKitInstanceSetting as MedicalKitInstanceSettingModel
from backend_common.models.medical_kit_instance_box_setting import MedicalKitInstanceBoxSetting as MedicalKitInstanceBoxSettingModel

medical_kit_instance_blueprint = Blueprint('medical_kit_instance', __name__)


class MedicalKitInstanceController(MedicalKitInstanceCommonController):

    @classmethod
    @get_request_params()
    def get(cls, data):
        medical_kit_instance_id = data.get('medical_kit_instance_id')
        medical_kit_instance = MedicalKitInstanceModel.select(MedicalKitInstanceModel.id, MedicalKitModel.product_code, MedicalKitModel.name, MedicalKitModel.image, MedicalKitModel.box_count).join(MedicalKitModel, on=(MedicalKitInstanceModel.product_code == MedicalKitModel.product_code)).dicts().first()
        setting = MedicalKitInstanceSettingModel.select().where(MedicalKitInstanceSettingModel.medical_kit_instance_id == medical_kit_instance_id).first()
        medical_kit_instance_box_settings = list(MedicalKitInstanceBoxSettingModel.select().where(MedicalKitInstanceBoxSettingModel.medical_kit_instance_id == medical_kit_instance_id).dicts())
        if medical_kit_instance:
            box_settings = []
            for i in range(1, medical_kit_instance.get('box_count')+1):
                if len(medical_kit_instance_box_settings):
                    box_setting = next(medical_kit_instance_box_setting for medical_kit_instance_box_setting in medical_kit_instance_box_settings if medical_kit_instance_box_setting.get('box_index') == i)
                    if box_setting:
                        box_setting.schedule_times = box_setting.schedule_times.split(',')
                        box_settings.append(box_setting)
                    else:
                        box_settings.append({'box_index': i, 'medical_name': '', 'medical_barcode': '', 'schedule_times': '', 'piece_per_time': 1, 'unit': '粒'})
                else:
                    box_settings.append({'box_index': i, 'medical_name': '', 'medical_barcode': '', 'schedule_times': [], 'piece_per_time': 1, 'unit': '粒'})
            medical_kit_instance.update({'setting': setting, 'box_settings': box_settings})
            return cls.success_with_result(medical_kit_instance)
        else:
            raise MedicalKitInstanceModel.NotFoundError('找不到该药箱')
