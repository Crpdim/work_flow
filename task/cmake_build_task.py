# task/cmake_build_task.py

from task.base_task import BaseTask
import subprocess

class CMakeBuildTask(BaseTask):
    def run(self):
        self.log("准备 CMake 构建...")
        remote_host = self.config['remote_host']
        remote_user = self.config['remote_user']
        remote_path = self.config['remote_path']
        cmake_options = self.config['cmake_options']
        build_dir = self.config['build_dir']
        project_name = self.config['project_name']  # 构建的项目名称
        
        def cmake_build_task():
            # 设置 CMake 构建命令
            cmake_command = f"ssh {remote_user}@{remote_host} 'cd {remote_path} && mkdir -p {build_dir} && cd {build_dir} && cmake .. {cmake_options} && make {project_name}'"
            subprocess.run(cmake_command, shell=True, check=True)
            self.log(f"项目 {project_name} 构建完成")
        
        # 使用重试逻辑
        self.retry_logic(cmake_build_task)
