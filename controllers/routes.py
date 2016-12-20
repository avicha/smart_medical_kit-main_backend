# coding=utf-8
from controllers.product_instance import product_instance_blueprint, ProductInstanceController


def init_app(current_app):
    # 管理员
    product_instance_blueprint.add_url_rule('/get', 'get_api', ProductInstanceController.get, methods=['get'])
    current_app.register_blueprint(product_instance_blueprint, url_prefix='/api/product_instance')
