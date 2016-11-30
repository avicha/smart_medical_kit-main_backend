# coding=utf-8
import env


class config:

    """前端相关配置"""

    def __init__(self, mode):
        if mode == 'development':
            self.driver = 'file'
            self.cache_dir = env.CACHE_FILE_DIR
            self.options = {
                'threshold': env.CACHE_FILE_THRESHOLD,
                'default_timeout': env.CACHE_DEFAULT_TIMEOUT,
                'mode': env.CACHE_FILE_MODE
            }
        elif mode == 'production':
            # self.driver = 'redis'
            # self.options = {
            #     'host': env.CACHE_REDIS_HOST,
            #     'port': env.CACHE_REDIS_HOST,
            #     'password': env.CACHE_REDIS_PASSWORD,
            #     'db': env.CACHE_REDIS_DB,
            #     'default_timeout': env.CACHE_DEFAULT_TIMEOUT,
            #     'key_prefix': env.CACHE_REDIS_KEY_PREFIX
            # }
            self.driver = 'file'
            self.cache_dir = env.CACHE_FILE_DIR
            self.options = {
                'threshold': env.CACHE_FILE_THRESHOLD,
                'default_timeout': env.CACHE_DEFAULT_TIMEOUT,
                'mode': env.CACHE_FILE_MODE
            }
