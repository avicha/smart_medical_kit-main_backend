# coding=utf-8
import sys
sys.path.append('.')
import pytest
from app import current_app
from flask import json


@pytest.fixture(scope="session")
def client():
    from backend_common.models.database import database
    current_app.config['TESTING'] = True
    with database.transaction() as txn:
        yield current_app.test_client()
        txn.rollback()


@pytest.fixture(scope="session")
def api_post(client):
    def f(url, *args, **kwargs):
        resp = client.post(url, *args, **kwargs)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        errcode = data.get('errcode')
        result = data.get('result')
        return errcode, result
    return f


@pytest.fixture(scope="session")
def api_get(client):
    def f(url, *args, **kwargs):
        resp = client.get(url, *args, **kwargs)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        errcode = data.get('errcode')
        result = data.get('result')
        return errcode, result
    return f


@pytest.fixture(scope="session")
def api_get_list(client):
    def f(url, *args, **kwargs):
        resp = client.get(url, *args, **kwargs)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        errcode = data.get('errcode')
        result = data.get('result')
        total_count = data.get('total_count')
        return errcode, result, total_count
    return f


@pytest.fixture
def medical_kit_instance():
    from backend_common.models.medical_kit_instance import MedicalKitInstance as MedicalKitInstanceModel
    medical_kit_instance = MedicalKitInstanceModel.select().where(MedicalKitInstanceModel.deleted_at == None).order_by(MedicalKitInstanceModel.created_at.desc()).first()
    return medical_kit_instance
