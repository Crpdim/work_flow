# main.py

from task_manager import TaskManager
from config import config

if __name__ == "__main__":
    task_manager = TaskManager(config)
    task_manager.execute()
