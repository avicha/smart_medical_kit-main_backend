# coding=utf-8
import time
from flask import Flask, g, request, request_started, request_finished
import json
import config


def config_secret_key(current_app):
    current_app.secret_key = config.server.secret_key


def config_log(current_app):
    import logging
    import logging.handlers
    if config.log.handler == 'time_rotating_file':
        LOG_FILE = config.log.log_dir + '/' + config.server.app_name + '.log'
        handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when=config.log.when, backupCount=config.log.backup_count)  # 实例化handler
    elif config.log.handler == 'stream':
        handler = logging.StreamHandler()
    # 实例化formatter
    formatter = logging.Formatter(config.log.format)
    # 为handler添加formatter
    handler.setFormatter(formatter)
    # 去掉flask默认的handler
    current_app.config['LOGGER_HANDLER_POLICY'] = 'never'
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


def config_routes(current_app):
    import controllers.routes
    controllers.routes.init_app(current_app)


def log_request(sender, **extra):
    g._start = time.time()
    data = request.json or request.form or request.args
    current_app.logger.info('\n%s "%s %s"，请求参数%s', request.remote_addr, request.method, request.url.encode('utf-8'), json.dumps(data))


def log_response(sender, response, **extra):
    dt = (time.time() - g._start)*1000
    try:
        resp = json.loads(response.response[0])
        errcode = resp.get('errcode')
        errmsg = resp.get('errmsg')
        total_count = resp.get('total_count')
        result = resp.get('result')
        if errcode == 0:
            if total_count != None:
                current_app.logger.info('耗时%.fms，请求API列表成功，返回结果：%s', dt, total_count)
            else:
                current_app.logger.info('耗时%.fms，请求API成功，返回结果：%s', dt, json.dumps(result))
        else:
            if errcode == 500:
                current_app.logger.error('耗时%.fms，发生系统未捕获错误，错误信息：%s', dt, errmsg.encode('utf-8'))
            else:
                current_app.logger.error('耗时%.fms，请求业务API出错，返回错误码%s，错误信息：%s', dt, errcode, errmsg.encode('utf-8'))
    except Exception, e:
        pass


def create_app():
    current_app = Flask(__name__)
    config_secret_key(current_app)
    config_log(current_app)
    config_errorhandler(current_app)
    config_cache(current_app)
    config_routes(current_app)
    request_started.connect(log_request, current_app)
    request_finished.connect(log_response, current_app)
    return current_app

current_app = create_app()


if __name__ == '__main__':
    current_app.run(config.server.host, config.server.port, config.server.debug, **config.server.options)
