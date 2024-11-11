# config.py

config = {
    "tasks": [
        {
            "name": "GitCloneMain", 
            "enabled": True, 
            "repo_url": "https://github.com/your/main-repo.git",
            "clone_path": "/path/to/main/repo",
            "max_retries": 3,
            "retry_delay": 5,
            "recover_on_failure": True
        },
        {
            "name": "GitCloneSource", 
            "enabled": True, 
            "source_repo_url": "https://github.com/your/thirdparty-repo.git",
            "source_clone_path": "/path/to/main/repo/source/thirdpart",
            "dependencies": ["GitCloneMain"],
            "max_retries": 2,
            "retry_delay": 10
        },
        {
            "name": "SFTPUpload", 
            "enabled": True,
            "local_path": "/path/to/main/repo",
            "remote_path": "/path/to/remote/project",
            "remote_host": "host.com",
            "remote_user": "user",
            "remote_password": "password",
            "dependencies": ["GitCloneSource"],
            "max_retries": 3,
            "retry_delay": 5
        },
        {
            "name": "CMakeBuild", 
            "enabled": True,
            "remote_host": "host.com",
            "remote_user": "user",
            "remote_path": "/path/to/project",
            "cmake_options": "-DCMAKE_BUILD_TYPE=Release",
            "build_dir": "build",
            "project_name": "project_name",  # 项目名称
            "dependencies": ["SFTPUpload"],
            "max_retries": 5,
            "retry_delay": 3,
            "recover_on_failure": False
        },
        {
            "name": "SFTPDownload", 
            "enabled": True,
            "remote_files": ["/path/to/remote/file1.elf"],  # ELF 文件列表
            "local_path": "/path/to/local/path",
            "remote_host": "host.com",
            "remote_user": "user",
            "remote_password": "password",
            "dependencies": ["CMakeBuild"],
            "max_retries": 3,
            "retry_delay": 5
        }
    ]
}
