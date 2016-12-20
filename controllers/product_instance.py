# coding=utf-8
from flask import Blueprint

from backend_common.middlewares.request_service import get_request_params
from backend_common.models.product import Product as ProductModel
from backend_common.models.sku import Sku as SkuModel
from backend_common.models.product_instance import ProductInstance as ProductInstanceModel
from backend_common.controllers.product_instance import ProductInstanceController as ProductInstanceCommonController

product_instance_blueprint = Blueprint('product_instance', __name__)


class ProductInstanceController(ProductInstanceCommonController):

    @classmethod
    @get_request_params()
    def get(cls, data):
        product_instance_id = data.get('product_instance_id')
        product_instance = ProductInstanceModel.select(ProductInstanceModel.product_code, SkuModel.id.alias('sku_id'), SkuModel.market_price.alias('sku_market_price'), SkuModel.sales_price.alias('sku_sales_price'), SkuModel.image.alias('sku_image'), SkuModel.props.alias('sku_props'), ProductModel.id.alias('product_id'), ProductModel.name.alias('product_name'), ProductModel.description.alias('product_description'), ProductModel.images.alias('product_images'), ProductModel.intro.alias('product_intro'), ProductModel.props.alias('product_props')).join(SkuModel, on=(ProductInstanceModel.sku_id == SkuModel.id)).join(ProductModel, on=(ProductModel.id == SkuModel.product_id)).where(ProductInstanceModel.product_code == product_instance_id).dicts().first()
        if product_instance:
            product_instance['sku_props'] = map(lambda x: {'k': x.split(':')[0], 'v': x.split(':')[1]}, product_instance.get('sku_props').split(';'))
            product_instance['product_props'] = map(lambda x: {'k': x.split(':')[0], 'v': x.split(':')[1]}, product_instance.get('product_props').split(';'))
            print product_instance['product_props']
        return cls.success_with_result(product_instance)
