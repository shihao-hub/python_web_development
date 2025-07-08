"""
# 需求背景
每次从 github 下载下来新代码后，都需要做一些前置操作，过于麻烦，为此选择 python 脚本帮忙实现这些功能

# 需求详情
- git init
  (如果已经初始化过，则跳过)
  - 否则，
    - git add .
    - git commit -m "initialize project"
- pip install -r requirements.txt
- python ./backend/manage.py makemigrations
- python ./backend/manage.py migrate
- python ./backend/manage.py createsuperuser --username admin
  注意，该命令需要输入 email address 和 2 次 password，此时应该需要一些进阶知识了
- 执行可能存在的 persistence.sql 文件，该文件为 django 项目数据库的序列化结果

tip:
- python.exe 需要改成 sys.executable，或者能否实现启动一个 git bash 但是执行多条命令？"command a;command b;command c"？
"""

import sys

executable: str = sys.executable
