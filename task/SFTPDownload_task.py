# task/sftp_download_task.py

import paramiko
import os
from task.Base_task import BaseTask

class SFTPDownloadTask(BaseTask):
    def run(self):
        remote_files = self.config['remote_files']  # ELF 文件列表
        local_path = self.config['local_path']
        remote_host = self.config['remote_host']
        remote_user = self.config['remote_user']

        def download_files():
            # 设置 SFTP 连接
            transport = paramiko.Transport((remote_host, 22))
            transport.connect(username=remote_user, password=self.config['remote_password'])
            sftp = paramiko.SFTPClient.from_transport(transport)

            try:
                for remote_file in remote_files:
                    local_file = os.path.join(local_path, os.path.basename(remote_file))
                    self.log(f"从远程下载文件 {remote_file} 到 {local_file}...")
                    sftp.get(remote_file, local_file)
                    self.log(f"文件 {remote_file} 下载完成")
            except Exception as e:
                self.log(f"下载失败: {e}")
                raise
            finally:
                sftp.close()
                transport.close()

        # 使用重试逻辑
        self.retry_logic(download_files)
