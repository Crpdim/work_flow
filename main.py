import argparse
import yaml
import logging
from task_manager import TaskManager

def load_config(flow_name):
    """加载指定的 YAML 配置文件"""
    try:
        with open(f"config/{flow_name}.yaml", 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"配置文件 {flow_name} 未找到")
        exit(1)
    except yaml.YAMLError as e:
        logging.error(f"加载 YAML 配置文件失败: {e}")
        exit(1)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="任务流水线")

    # 参数 -t 用于指定任务流配置文件，默认为 default_config
    parser.add_argument('-t', '--taskflow', type=str, default='default_config', help="指定任务流名称 (默认：default)")

    # 参数 -p 用于传递任务参数 (key=value)，可以指定修改配置文件中的某些值
    parser.add_argument('-p', '--param', action='append', help="任务参数键值对，例如 repo_url=https://github.com/your/repo.git")

    return parser.parse_args()

def apply_params(config, params):
    """应用命令行传递的参数，覆盖配置文件中的值"""
    if params:
        param_pairs = params[0].split()
        for param in param_pairs:
            key, value = param.split("=")
            # 遍历配置文件，找到对应的任务并修改参数
            for task in config['tasks']:
                if key in task:
                    task[key] = value
                    logging.info(f"参数 {key} 被修改为 {value}")
                    break
                else:
                    logging.warning(f"未找到参数 {key}，忽略修改")

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()
    flow_name = args.taskflow  # 获取任务流名称
    params = args.param  # 获取任务参数

    # 加载配置文件
    config = load_config(flow_name)

    # 应用命令行传递的参数
    apply_params(config, params)

    # 初始化任务管理器，并传入指定的任务配置
    task_manager = TaskManager(config)
    task_manager.execute()
