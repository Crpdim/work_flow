import argparse
import yaml
import logging
import sys
from task_manager import TaskManager

def load_config(flow_name):
    """加载指定的 YAML 配置文件"""
    config_file = f"config/{flow_name}.yaml"
    try:
        # 使用 UTF-8 编码打开配置文件
        with open(config_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"配置文件 {config_file} 未找到")
        sys.exit(1)  # 更标准的退出方式
    except yaml.YAMLError as e:
        logging.error(f"加载 YAML 配置文件失败: {e}")
        sys.exit(1)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="任务流水线")

    # 参数 -t 用于指定任务流配置文件，默认为 default_config
    parser.add_argument('-t', '--taskflow', type=str, default='default_config', help="指定任务流名称 (默认：default_config)")

    # 参数 -p 用于传递任务参数 (key=value)，可以指定修改配置文件中的某些值
    parser.add_argument('-p', '--param', action='append', help="任务参数键值对，例如 repo_url=https://github.com/your/repo.git")

    return parser.parse_args()

def apply_params(config, params):
    """应用命令行传递的参数，覆盖配置文件中的值"""
    if params:
        for param in params:
            try:
                key, value = param.split("=")
                applied = False
                # 遍历配置文件中的每个任务
                for task in config['tasks']:
                    if key in task:
                        task[key] = value
                        logging.info(f"参数 {key} 被修改为 {value}")
                        applied = True
                        break
                if not applied:
                    logging.warning(f"未找到参数 {key}，忽略修改")
            except ValueError:
                logging.error(f"无效的参数格式: {param}，正确格式为 key=value")
                
def setup_logging():
    """配置日志格式和级别"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    # 设置日志
    setup_logging()

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
