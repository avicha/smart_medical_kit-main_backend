# coding=utf-8
import env


class config:

    """服务器配置"""

    def __init__(self, mode):
        if mode == 'development':
            self.handler = 'stream'
            self.format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
            self.level = 'DEBUG'
        elif mode == 'production':
            self.handler = 'time_rotating_file'
            self.format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
            self.level = 'INFO'
            self.log_dir = env.LOG_FILE_DIR
            self.when = env.LOG_FILE_WHEN
            self.backup_count = env.LOG_FILE_BACKUP_COUNT
