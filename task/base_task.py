# task/base_task.py

import time
import logging

class BaseTask:
    def __init__(self, config):
        self.config = config
        self.is_completed = False

    def log(self, message):
        logging.info(message)

    def retry_logic(self, task_func):
        max_retries = self.config.get("max_retries", 3)
        retry_delay = self.config.get("retry_delay", 5)
        recover_on_failure = self.config.get("recover_on_failure", False)
        
        attempt = 0
        while attempt < max_retries:
            try:
                task_func()
                break  # 如果任务成功，退出重试
            except Exception as e:
                attempt += 1
                self.log(f"任务失败，重试 {attempt}/{max_retries}，错误: {e}")
                if attempt >= max_retries:
                    if recover_on_failure:
                        self.recover()
                    raise e  # 如果达到最大重试次数，抛出异常
                time.sleep(retry_delay)

    def recover(self):
        """任务失败后的恢复逻辑"""
        self.log(f"执行任务失败后的恢复操作: {self.config['name']}")
        # 在此处可以定义如何恢复任务，例如清理临时文件、重置状态等



"""
# task/base_task.py
from plyer import notification
import logging
import time

class BaseTask:
    def __init__(self, config):
        self.config = config
        self.is_completed = False

    def log(self, message):
        logging.info(message)

    def notify_failure(self, task_name, error_message):
        # 任务失败时弹出 Windows 通知
        notification.notify(
            title=f"任务失败: {task_name}",
            message=error_message,
            timeout=10  # 通知显示的时间（秒）
        )

    def retry_logic(self, task_func):
        max_retries = self.config.get("max_retries", 3)
        retry_delay = self.config.get("retry_delay", 5)
        recover_on_failure = self.config.get("recover_on_failure", False)
        
        attempt = 0
        while attempt < max_retries:
            try:
                task_func()
                break  # 如果任务成功，退出重试
            except Exception as e:
                attempt += 1
                self.log(f"任务失败，重试 {attempt}/{max_retries}，错误: {e}")
                if attempt >= max_retries:
                    if recover_on_failure:
                        self.recover()
                    # 调用 Windows 弹窗提醒
                    self.notify_failure(self.config['name'], str(e))
                    raise e  # 如果达到最大重试次数，抛出异常
                time.sleep(retry_delay)

    def recover(self):
        # 任务失败后的恢复逻辑
        self.log(f"执行任务失败后的恢复操作: {self.config['name']}")
        # 在此处可以定义如何恢复任务，例如清理临时文件、重置状态等

"""