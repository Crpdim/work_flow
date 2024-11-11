# task/git_clone_source_task.py

from task.base_task import BaseTask
import subprocess
import os

class GitCloneSourceTask(BaseTask):
    def run(self):
        self.log("开始克隆 source 仓库...")
        repo_url = self.config['source_repo_url']
        source_clone_path = self.config['source_clone_path']
        
        def clone_source_task():
            if not os.path.exists(source_clone_path):
                self.log("source 仓库不存在，开始克隆...")
                subprocess.run(['git', 'clone', repo_url, source_clone_path], check=True)
                self.log("source Git 克隆完成")
            else:
                self.log("source 仓库已存在，执行 git pull 更新仓库...")
                subprocess.run(['git', 'pull'], cwd=source_clone_path, check=True)
                self.log("source Git pull 完成，仓库已更新")
        
        # 使用重试逻辑
        self.retry_logic(clone_source_task)
