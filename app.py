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


def log_response(sender, response, **extra):
    g._end = time.time()
    dt = (g._end - g._start)*1000
    data = request.json or request.form or request.args
    data_str = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')).encode('utf-8')
    try:
        resp = json.loads(response.response[0])
        errcode = resp.get('errcode')
        errmsg = resp.get('errmsg')
        if errcode == 0:
            current_app.logger.info('%s "%s %s"，开始请求时间：%s，结束时间：%s，耗时%.fms，请求API成功，请求参数：\n%s', request.remote_addr, request.method, request.url.encode('utf-8'),  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(g._end)), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(g._start)), dt, data_str)
        else:
            if errcode == 500:
                current_app.logger.error('耗时%.fms，发生系统未捕获错误，错误信息：%s，请求参数：\n%s', dt, errmsg.encode('utf-8'), data_str)
            else:
                current_app.logger.error('耗时%.fms，请求业务API出错，返回错误码%s，错误信息：%s，请求参数：\n%s', dt, errcode, errmsg.encode('utf-8'), data_str)
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
