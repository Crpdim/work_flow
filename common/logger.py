import logging
import os

class Logger:
    def __init__(self, log_dir="logs", log_file="task_log.txt", log_level=logging.INFO):
        # 日志文件夹路径，如果不存在则创建
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 日志文件路径
        self.log_file = os.path.join(log_dir, log_file)

        # 创建日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # 创建文件处理器，将日志写入文件
        file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # 创建控制台处理器，输出到控制台
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(log_level)
        # console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # 将处理器添加到日志记录器
        self.logger.addHandler(file_handler)
        # self.logger.addHandler(console_handler)
        
        # self.log("日志系统初始化")

    def log(self, message, level=logging.INFO):
        """记录日志消息"""
        self.logger.log(level, message)

    def exception(self, message, exc_info=True):
        """记录异常日志"""
        self.logger.error(message, exc_info=exc_info)

# 创建一个全局日志实例
log_instance = Logger()

# 提供简易的接口来记录日志
def log(message, level=logging.INFO):
    log_instance.log(message, level)

def exception(message):
    log_instance.exception(message)
