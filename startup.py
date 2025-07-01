import configparser
import os
import sys

config = configparser.ConfigParser()
config.read("./conf/config.ini")

BACNEND_PORT = config.getint("settings", "backend_port")

# 项目路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_CMD = ["python", "main.py"]
BACKEND_CMD = ["python", "manage.py", "runserver", "8888"]

executable = sys.executable

# todo: 我认为肯定有第三方库，当然自己也能实现一份（ai 输出的好多，看样子完备实现很复杂）

# 启动 frontend：python ./frontend/main.py

# 启动 backend：python ./backend/manage.py runserver 8888
