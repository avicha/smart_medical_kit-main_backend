# coding=utf-8

from flask import Flask, redirect, url_for, g, jsonify
import config


def config_secret_key(current_app):
    current_app.secret_key = config.server.secret_key


def config_log(current_app):
    import logging
    import logging.handlers
    if config.log.handler == 'time_rotating_file':
        LOG_FILE = config.log.log_dir + '/main.log'
        handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when=config.log.when, backupCount=config.log.backup_count)  # 实例化handler
    elif config.log.handler == 'stream':
        handler = logging.StreamHandler()
    # 实例化formatter
    formatter = logging.Formatter(config.log.format)
    # 为handler添加formatter
    handler.setFormatter(formatter)
    # 为logger添加handler
    current_app.logger.addHandler(handler)
    # 设置logger的显示级别
    current_app.logger.setLevel(config.log.level)


def config_errorhandler(current_app):
    import backend_common.exceptions
    backend_common.exceptions.init_app(current_app)


def config_cache(current_app):
    import werkzeug.contrib.cache
    if config.cache.driver == 'simple':
        cache = werkzeug.contrib.cache.SimpleCache(**config.cache.options)
    elif config.cache.driver == 'memcache':
        cache = werkzeug.contrib.cache.MemcachedCache(**config.cache.options)
    elif config.cache.driver == 'redis':
        cache = werkzeug.contrib.cache.RedisCache(**config.cache.options)
    elif config.cache.driver == 'file':
        cache = werkzeug.contrib.cache.FileSystemCache(config.cache.cache_dir, **config.cache.options)
    else:
        cache = werkzeug.contrib.cache.NullCache(**config.cache.options)
    current_app.cache = cache


def load_user(current_app):
    @current_app.before_request
    def load_user():
        from flask import request, g
        from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
        from backend_common.models.user import User as UserModel
        data = request.json or request.form or request.args
        if data.get('token'):
            token = data.get('token')
            s = TimedJSONWebSignatureSerializer(config.server.secret_key)
            try:
                user_id = s.loads(token)
                user = UserModel.get(UserModel.id == user_id, UserModel.deleted_at == None)
                tokens = user.tokens()
                if token in tokens:
                    g.user = user
                    return None
                else:
                    raise UserModel.TokenError('请重新登录')
            except SignatureExpired:
                raise UserModel.TokenError('登录已经过期')
            except BadSignature:
                raise UserModel.PasswordError()
            except UserModel.DoesNotExist, e:
                raise UserModel.NotFoundError('该用户不存在')
        else:
            g.user = None
            return None


def config_routes(current_app):
    import controllers.routes
    controllers.routes.init_app(current_app)


def create_app():
    current_app = Flask(__name__)
    config_secret_key(current_app)
    config_log(current_app)
    config_errorhandler(current_app)
    config_cache(current_app)
    load_user(current_app)
    config_routes(current_app)
    return current_app

current_app = create_app()

if __name__ == '__main__':
    current_app.run(config.server.host, config.server.port, config.server.debug, **config.server.options)
