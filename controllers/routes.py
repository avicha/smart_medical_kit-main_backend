# coding=utf-8
from controllers.user import user_blueprint, UserController
from controllers.service import service_blueprint, ServiceController


def init_app(current_app):
    # 服务
    service_blueprint.add_url_rule('/send_verifycode', 'send_verifycode_api', ServiceController.send_verifycode, methods=['get'])
    current_app.register_blueprint(service_blueprint, url_prefix='/api/service')
    # 用户
    user_blueprint.add_url_rule('/register', 'register_api', UserController.register, methods=['post'])
    user_blueprint.add_url_rule('/login', 'login_api', UserController.login, methods=['post'])
    user_blueprint.add_url_rule('/logout', 'logout_api', UserController.logout, methods=['get'])
    user_blueprint.add_url_rule('/reset_password', 'reset_password_api', UserController.reset_password, methods=['post'])
    user_blueprint.add_url_rule('/current', 'current_api', UserController.current, methods=['get'])
    user_blueprint.add_url_rule('/update', 'update_api', UserController.update, methods=['post'])
    current_app.register_blueprint(user_blueprint, url_prefix='/api/user')
