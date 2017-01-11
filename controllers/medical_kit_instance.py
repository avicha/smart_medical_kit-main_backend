# coding=utf-8
from flask import Blueprint

from backend_common.controllers.medical_kit_instance import MedicalKitInstanceController as MedicalKitInstanceCommonController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.database import database
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
        medical_kit_instance_model = MedicalKitInstanceModel(id=medical_kit_instance_id)
        medical_kit_instance = MedicalKitInstanceModel.select(MedicalKitInstanceModel.id, MedicalKitModel.product_code, MedicalKitModel.name, MedicalKitModel.image, MedicalKitModel.box_count).join(MedicalKitModel, on=(MedicalKitInstanceModel.product_code == MedicalKitModel.product_code)).where(MedicalKitInstanceModel.id == medical_kit_instance_id).dicts().first()
        if medical_kit_instance:
            setting = medical_kit_instance_model.setting()
            box_settings = medical_kit_instance_model.box_settings(medical_kit_instance.get('box_count'))
            medical_kit_instance.update({'setting': setting, 'box_settings': box_settings})
            return cls.success_with_result(medical_kit_instance)
        else:
            raise MedicalKitInstanceModel.NotFoundError('找不到该药箱')

    @classmethod
    @get_request_params()
    def set_setting(cls, data):
        medical_kit_instance_id = data.get('medical_kit_instance_id')
        setting = data.get('setting')
        box_settings = data.get('box_settings')
        with database.transaction():
            medical_kit_instance_setting = MedicalKitInstanceSettingModel.select().where(MedicalKitInstanceSettingModel.medical_kit_instance_id == medical_kit_instance_id).for_update().first()
            if medical_kit_instance_setting:
                medical_kit_instance_setting.prompt_sound = setting.get('prompt_sound')
                medical_kit_instance_setting.save()
            else:
                MedicalKitInstanceSettingModel.create(medical_kit_instance_id=medical_kit_instance_id, prompt_sound=setting.get('prompt_sound'))
            for box_setting in box_settings:
                if len(box_setting.get('schedule_times')):
                    medical_kit_instance_box_setting = MedicalKitInstanceBoxSettingModel.select().where(MedicalKitInstanceBoxSettingModel.medical_kit_instance_id == medical_kit_instance_id, MedicalKitInstanceBoxSettingModel.box_index == box_setting.get('box_index')).for_update().first()
                    if medical_kit_instance_box_setting:
                        medical_kit_instance_box_setting.medical_name = box_setting.get('medical_name')
                        medical_kit_instance_box_setting.medical_barcode = box_setting.get('medical_barcode')
                        medical_kit_instance_box_setting.schedule_times = ','.join(box_setting.get('schedule_times'))
                        medical_kit_instance_box_setting.piece_per_time = box_setting.get('piece_per_time')
                        medical_kit_instance_box_setting.unit = box_setting.get('unit')
                        medical_kit_instance_box_setting.save()
                    else:
                        MedicalKitInstanceBoxSettingModel.create(medical_kit_instance_id=medical_kit_instance_id, box_index=box_setting.get('box_index'), medical_name=box_setting.get('medical_name'), medical_barcode=box_setting.get('medical_barcode'), schedule_times=','.join(box_setting.get('schedule_times')), piece_per_time=box_setting.get('piece_per_time'), unit=box_setting.get('unit'))
            return cls.success_with_result(None)
