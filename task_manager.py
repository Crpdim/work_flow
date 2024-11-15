from common.logger import log
from task_loader import TaskLoader
import logging

class TaskManager:
    def __init__(self, config):
        self.config = config
        self.task_loader = TaskLoader(self.config)  # 加载任务
        self.tasks = self.task_loader.load_tasks()  # 加载任务实例

    def execute(self):
        for task in self.tasks:
            if self.check_dependencies(task):
                self.execute_task(task)

    def check_dependencies(self, task):
        dependencies = task.config.get("dependencies", [])
        for dep_task_name in dependencies:
            dep_task = self.get_task_by_name(dep_task_name)
            if not dep_task.is_completed:
                log(f"任务 {task.config['name']} 的依赖 {dep_task_name} 尚未完成，跳过执行", logging.WARN)
                return False
        return True

    def get_task_by_name(self, task_name):
        for task in self.tasks:
            if task.config["name"] == task_name:
                return task
        return None

    def execute_task(self, task):
        log(f"开始执行任务: {task.config['name']}")
        try:
            task.run()
            task.is_completed = True
            log(f"任务 {task.config['name']} 执行成功")
        except Exception as e:
            log(f"任务 {task.config['name']} 执行失败: {e}", logging.ERROR)
            task.is_completed = False
