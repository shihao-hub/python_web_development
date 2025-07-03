"""
[安装包](https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/deploy/package.html)

pyinstaller -F -D ./main.py

还有更多补充内容，需要完善

--onefile

pyinstaller --name myapp --add-data "D:/JetBrainsProjects/PycharmProjects/PyCharm-python_web_development-main/python_web_development-main0/.venv/Lib/site-packages/nicegui;nicegui" main.py


"""
import asyncio
import ctypes
import os
import shutil
import shlex
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional

from loguru import logger

VENV_PATH = Path(sys.executable).parent.parent

# todo: 解决命令中 "\J" 会被视为一个转义字符的问题
ADD_DATA_OPTION = f'"{VENV_PATH / "Lib" / "site-packages" / "nicegui"};nicegui"'.replace("\\", "/")
PYINSTALLER_PATH = f'"{VENV_PATH / "Scripts" / "pyinstaller.exe"}"'.replace("\\", "/")
APP_NAME = "myapp" + "_" + str(int(time.time()))
ENTRANCE_PATH = str(Path(__file__).resolve().parent / "main.py").replace("\\", "/")

PYINSTALLER_COMMAND: str = (f'{PYINSTALLER_PATH} '
                            f'--name {APP_NAME} '
                            f'--add-data {ADD_DATA_OPTION} '
                            f'"{ENTRANCE_PATH}"')

# fixme: 解决 PYINSTALLER_COMMAND 超出 Windows 系统默认限制路径长度为 260 个字符的问题，默认的 cmd 似乎没有启用长路径支持
logger.info("PyInstaller Command: {}", PYINSTALLER_COMMAND)


def find_git_bash():
    """查找 Git Bash 的安装路径"""
    possible_paths = [
        os.path.expandvars(r"%ProgramFiles%\Git\bin\bash.exe"),
        os.path.expandvars(r"%ProgramFiles%\Git\git-bash.exe"),
        os.path.expandvars(r"%LocalAppData%\Programs\Git\bin\bash.exe"),
        r"D:\Software\Git\bin\bash.exe"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # 尝试通过系统 PATH 查找
    bash_path = shutil.which("git-bash.exe") or shutil.which("bash.exe")
    if bash_path:
        return bash_path

    raise FileNotFoundError("无法找到 Git Bash 可执行文件")


git_bash_path = find_git_bash()
logger.info("git_bash_path: {}", git_bash_path)


# [important] 异步 subprocess！很好！很妙！
async def run_async_command(
        command: str,
        timeout: Optional[float] = None,
        cwd: Optional[str] = None,
        env: Optional[dict] = None
) -> int:
    """
    异步执行命令并实时输出

    参数:
        command (str): 要执行的命令
        timeout (float): 命令执行超时时间（秒）
        cwd (str): 工作目录
        env (dict): 环境变量

    返回:
        int: 命令的退出码
    """
    # 创建子进程
    logger.debug("{}", f'"{git_bash_path}" --login -c {command}')
    # todo: 确认一下，这个 windows 上默认是不是启动的 cmd？
    process = await asyncio.create_subprocess_shell(
        # f'{command} | "{git_bash_path}"',
        # 注意，{command} 需要用引号包裹起来，才是一个命令！而且得用单引号，因为 command 内有双引号
        f'{git_bash_path} --login -c \'{command}\'',
        # 当设置为 True 时，命令通过系统的 shell 执行（如 /bin/sh 或 cmd.exe）
        # 优点：支持 shell 特性（管道、重定向、环境变量扩展等）
        # 缺点：有安全风险（如果命令包含用户输入），建议只用于受信任的命令
        # shell=True,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    # 实时读取输出
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        logger.info(line.decode().rstrip())

    # 等待进程结束
    await process.wait()
    return process.returncode


if __name__ == "__main__":
    asyncio.run(run_async_command(PYINSTALLER_COMMAND))
