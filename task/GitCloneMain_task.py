# task/git_clone_main_task.py

from task.Base_task import BaseTask
import subprocess
import os

class GitCloneMainTask(BaseTask):
    def run(self):
        self.log("开始克隆主仓库...")
        repo_url = self.config['repo_url']
        clone_path = self.config['clone_path']
        
        def clone_task():
            if not os.path.exists(clone_path):
                self.log("仓库不存在，开始克隆...")
                subprocess.run(['git', 'clone', '-b', 'master', repo_url, clone_path], check=True)
                self.log("Git 克隆完成")
            else:
                self.log("仓库已存在，执行 git pull 更新仓库...")
                subprocess.run(['git', 'pull'], cwd=clone_path, check=True)
                self.log("Git pull 完成，仓库已更新")
        
        # 使用重试逻辑
        self.retry_logic(clone_task)


""" 
# task/git_clone_main_task.py

from task.Base_task import BaseTask
import subprocess
import os

class GitCloneMainTask(BaseTask):
    def run(self):
        self.log("开始克隆主仓库...")
        repo_url = self.config['repo_url']
        clone_path = self.config['clone_path']
        
        def clone_task():
            if not os.path.exists(clone_path):
                self.log("仓库不存在，开始克隆...")
                subprocess.run(['git', 'clone', '-b', 'master', repo_url, clone_path], check=True)
                self.log("Git 克隆完成")
            else:
                self.log("仓库已存在，执行 git pull 更新仓库...")
                subprocess.run(['git', 'pull'], cwd=clone_path, check=True)
                self.log("Git pull 完成，仓库已更新")
        
        # 使用重试逻辑
        self.retry_logic(clone_task)

Yaml
tasks:
  - name: GitCloneMain
    enabled: true
    repo_url: "git@github.com:your/repo.git"  # SSH 地址
    clone_path: "/path/to/main/repo"
    ssh_key_path: "/path/to/your/ssh_key"  # SSH key 的路径
    ssh_key_passphrase: "your_passphrase"  # 如果 SSH key 有 passphrase 可设置
    max_retries: 3
    retry_delay: 5
    recover_on_failure: True

"""