# coding=utf-8

from flask import Blueprint
from backend_common.controllers.service import ServiceController as ServiceCommonController

service_blueprint = Blueprint('service', __name__)


class ServiceController(ServiceCommonController):
    pass
