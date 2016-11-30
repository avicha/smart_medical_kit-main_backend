# coding=utf-8
import env


class config:

    """服务器配置"""

    def __init__(self, mode):
        self.host = env.SERVER_HOST
        self.port = env.SERVER_PORT
        self.debug = env.SERVER_DEBUG
        self.options = {
            'use_reloader': env.SERVER_USE_RELOADER,
            'use_debugger': env.SERVER_USE_DEBUGGER,
        }
        self.secret_key = env.SECRET_KEY
