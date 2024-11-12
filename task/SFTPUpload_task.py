# task/sftp_upload_task.py

import paramiko
from task.Base_task import BaseTask

class SFTPUploadTask(BaseTask):
    def run(self):
        local_path = self.config['local_path']
        remote_path = self.config['remote_path']
        remote_host = self.config['remote_host']
        remote_user = self.config['remote_user']
        
        def upload_file():
            # 设置 SFTP 连接
            transport = paramiko.Transport((remote_host, 22))
            transport.connect(username=remote_user, password=self.config['remote_password'])
            sftp = paramiko.SFTPClient.from_transport(transport)

            try:
                self.log(f"上传文件到远端 {remote_path}...")
                sftp.put(local_path, remote_path)
                self.log("文件上传成功")
            except Exception as e:
                self.log(f"上传失败: {e}")
                raise
            finally:
                sftp.close()
                transport.close()

        # 使用重试逻辑
        self.retry_logic(upload_file)
