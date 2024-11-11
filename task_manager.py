# task_manager.py

import importlib
import logging

class TaskManager:
    def __init__(self, config):
        self.config = config
        self.tasks = self.load_tasks()

    def load_tasks(self):
        tasks = []
        for task_config in self.config["tasks"]:
            if task_config.get("enabled", False):
                task_name = task_config["name"]
                task_module = importlib.import_module(f"task.{task_name.lower()}_task")
                task_class = getattr(task_module, f"{task_name}Task")
                task_instance = task_class(task_config)
                tasks.append(task_instance)
        return tasks

    def execute(self):
        logging.basicConfig(level=logging.INFO)
        for task in self.tasks:
            if self.check_dependencies(task):
                self.execute_task(task)

    def check_dependencies(self, task):
        # 检查依赖任务是否已经完成
        if "dependencies" in task.config:
            for dep_task_name in task.config["dependencies"]:
                dep_task = self.get_task_by_name(dep_task_name)
                if not dep_task.is_completed:
                    logging.warning(f"任务 {task.config['name']} 的依赖 {dep_task_name} 尚未完成，跳过执行")
                    return False
        return True

    def get_task_by_name(self, task_name):
        for task in self.tasks:
            if task.config["name"] == task_name:
                return task
        return None

    def execute_task(self, task):
        logging.info(f"开始执行任务: {task.config['name']}")
        try:
            task.run()
            task.is_completed = True
            logging.info(f"任务 {task.config['name']} 执行成功")
        except Exception as e:
            logging.error(f"任务 {task.config['name']} 执行失败: {e}")
            task.is_completed = False
