# task/git_clone_main_task.py

from task.Base_task import BaseTask
import subprocess
import os

class GitCloneMainTask(BaseTask):
    def run(self):
        self.log("开始克隆主仓库...")
        repo_url = self.config['repo_url']
        clone_path = self.config['clone_path']
        private_key_path = self.config['private_key_path']

        def clone_task():
            # 设置 GIT_SSH_COMMAND 以使用私钥
            env = os.environ.copy()
            env["GIT_SSH_COMMAND"] = f"ssh -i {private_key_path} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
            # 判断目录是否存在且是否是一个 Git 仓库
            if not os.path.exists(clone_path) or not os.path.isdir(os.path.join(clone_path, '.git')):
                self.log("仓库不存在或不是一个 Git 仓库，开始克隆...")
                try:
                    subprocess.run(['git', 'clone', repo_url, clone_path], check=True, env=env) 
                    self.log("Git 克隆完成")
                except subprocess.CalledProcessError as e:
                    self.log(f"更新仓库时发生错误: {e.stderr}")
            else:
                self.log("仓库已存在，执行 git pull 更新仓库...")
                # 判断仓库是否是最新的
                try:
                    subprocess.run(['git', 'fetch'], cwd=clone_path, check=True, env=env) 
                    # 获取当前分支的最新提交与远程的比较
                    status = subprocess.check_output(['git', 'status', '-uno'], cwd=clone_path, env=env)
                    if b'Your branch is up to date' in status:
                        self.log("仓库已经是最新的")
                    else:
                        self.log("仓库不是最新的，执行 git pull 更新仓库...")
                        subprocess.run(['git', 'pull'], cwd=clone_path, check=True, env=env) 
                    self.log("Git pull 完成，仓库已更新")
                except subprocess.CalledProcessError as e:
                    self.log(f"更新仓库时发生错误: {e.stderr}")
        
        # 使用重试逻辑
        self.retry_logic(clone_task)

