# coding=utf-8
from flask import Blueprint

from backend_common.controllers.medical import MedicalController as MedicalCommonController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.medical import Medical as MedicalModel
from backend_common.services.medical import MedicalAPI

medical_blueprint = Blueprint('medical', __name__)


class MedicalController(MedicalCommonController):

    @classmethod
    @get_request_params()
    def scan(cls, data):
        barcode = data.get('barcode')
        medical = MedicalModel.select().where(MedicalModel.barcode == barcode).first()
        if medical:
            result = medical.format()
            return cls.success_with_result(result)
        else:
            medical_info = MedicalAPI.scan(barcode)
            medical = MedicalModel.create(**medical_info)
            result = medical.format()
            return cls.success_with_result(result)
