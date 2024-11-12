import importlib
import logging

class TaskLoader:
    def __init__(self, config):
        self.config = config

    def load_tasks(self):
        tasks = []
        for task_config in self.config["tasks"]:
            if task_config.get("enabled", False):
                task_instance = self.create_task_instance(task_config)
                if task_instance:
                    tasks.append(task_instance)
                else:
                    logging.warning(f"任务 {task_config['name']} 加载失败")
        return tasks

    def create_task_instance(self, task_config):
        """根据任务配置动态加载任务类"""
        task_name = task_config["name"]
        try:
            task_class = self.load_task_class(task_name)
            return task_class(task_config)
        except Exception as e:
            logging.error(f"创建任务实例 {task_name} 时发生错误: {e}")
            return None

    def load_task_class(self, task_name):
        """根据任务名称加载对应的任务类"""
        task_module_name = task_name + "_task"
        task_class_name = task_name + "Task"

        # 动态导入任务模块和任务类
        task_module = importlib.import_module(f"task.{task_module_name}")
        task_class = getattr(task_module, task_class_name)

        return task_class
