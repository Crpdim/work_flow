import subprocess
from task.Base_task import BaseTask

class ShellCommandTask(BaseTask):
    def __init__(self, config):
        super().__init__(config)
        self.commands = config.get("commands", [])  # 获取命令列表

    def run(self):
        """按顺序执行命令"""
        self.log("开始执行 Shell 操作...")
        
        def execute_command(command):
            """执行单个命令并处理异常"""
            try:
                self.log(f"正在执行命令: {command}")
                subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  # 使用 shell 执行命令
                self.log(f"命令执行成功: {command}")
            except subprocess.CalledProcessError as e:
                self.log(f"命令执行失败: {command}, 错误: {e.stderr}")
                raise e  # 可以选择在命令失败时停止执行或进行恢复处理
        
        # 遍历命令列表，按顺序执行
        for command in self.commands:
            # 使用重试逻辑执行命令
            self.retry_logic(lambda: execute_command(command))

        self.log("所有 Shell 操作执行完成.")

# 配置示例
"""
tasks:
  - name: ExecuteShellCommands
    enabled: true
    commands:
      - "echo 'Hello, World!'"
      - "mkdir -p /path/to/dir"
      - "git clone https://github.com/your/repo.git"
    max_retries: 3
    retry_delay: 5
    recover_on_failure: True
"""

