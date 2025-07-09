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
- python ./backend/manager.py makemigrations
- python ./backend/manager.py migrate
- python ./backend/manager.py createsuperuser --username admin
  注意，该命令需要输入 email address 和 2 次 password，此时应该需要一些进阶知识了
  （如果命令需要交互式输入（如 ssh、ftp），可以使用 communicate()）
- 执行可能存在的 persistence.sql 文件，该文件为 django 项目数据库的序列化结果

tip:
- python.exe 需要改成 sys.executable，或者能否实现启动一个 git bash 但是执行多条命令？"command a;command b;command c"？

"""
import copy
import msvcrt
import os.path
import sys
import subprocess
from pathlib import Path
from typing import List, Union

from loguru import logger


def version_1_0():
    # 试图实现需求，但是效率极低，成果极低，且出现未知问题，遂放弃，选择先问 ai 再进行下一步。【善用工具，抛弃学生思维】
    executable: str = sys.executable
    pip_path: str = str(Path(sys.executable).resolve().parent / "Scripts" / "pip.exe")

    # Windows 上激活虚拟环境：..\python_web_development-main\.venv\Scripts\activate

    working_directory: str = str(Path(__file__).parent)
    logger.debug("working_directory: {}", working_directory)

    COMMANDS = [  # noqa: Variable in function should be lowercase
        f"git init",
        f"git add .",
        f'git commit -m "initialize project"',
        # 推荐列表形式避免注入风险
        [pip_path, "install", "-r", os.path.join(working_directory, "requirements.txt")],
        [executable, os.path.join(working_directory, "backend", "manager.py"), "makemigrations"],
        [executable, os.path.join(working_directory, "backend", "manager.py"), "migrate"],
    ]

    for command in COMMANDS:
        try:
            # subprocess.run 应该是封装了 subprocess.Popen 和 process.communicate，灵活性不够，似乎无法实现实时读取输出
            result = subprocess.run(
                command,
                cwd=working_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            # todo: 待解决，总是执行失败
            #       - 时间有限，subprocess 只能带着学习
            #       - 今天花了一小时，毫无成果，需要总结一下
            #         - 我认为，除非系统学习 subprocess，否则推荐将自己的需求详细告诉 ai，这是初步做法
            #         - 如果 ai 没有办法解决，则在 ai 的基础上，查询资料进一步解决，这是最终做法

            # 按行统一分割输出
            for line in result.stdout.splitlines():
                logger.info("{}", line.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            logger.error("执行 `{}` 失败：{}", command, e.stderr)
        except Exception as e:
            logger.error("UnExpected Exception - 执行 `{}` 失败：{}", command, e)
            # raise e
        else:
            logger.info("命令 `{}` 执行成功", command)


def main():
    import subprocess
    import sys
    import time
    import getpass
    from pathlib import Path
    import signal

    # 设置颜色代码
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def print_header(text):
        """打印带样式的标题"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")

    def print_success(text):
        """打印成功信息"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

    def print_warning(text):
        """打印警告信息"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

    def print_error(text):
        """打印错误信息"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

    def print_step(text):
        """打印步骤信息"""
        print(f"{Colors.OKCYAN}→ {text}{Colors.ENDC}")

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #

    def run_command(command: Union[str, List[str]], capture_output=False, cwd=None, shell=False):
        """运行命令并返回结果"""
        old_command = command
        try:
            command = copy.deepcopy(old_command)

            # ------------------------ command 内容转换 ------------------------ #
            # python 改为绝对路径
            if isinstance(command, List) and command[0].strip() == "python":
                command[0] = f'{sys.executable}'
            # ./ 开头的路径转为绝对路径
            for i in range(len(command)):
                if not command[i].strip().startswith("./"):
                    continue
                cwd = os.path.abspath("./")
                # command[i] 切割
                path_parts = Path(command[i]).parts
                new_path = Path(cwd)
                for part in path_parts:
                    new_path = new_path / part
                command[i] = f'{new_path}'
            print(f"command: {command}")

            # 捕获输出的意思应该是控制台不答应，被管道捕获了，目的应该是为了进程协同，将当前进程输出通过管道传递给下一个进程？
            if capture_output:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=cwd,
                    shell=shell
                )
                return result
            else:
                subprocess.run(command, check=True, cwd=cwd, shell=shell)
                return True
        except subprocess.CalledProcessError as e:
            print_error(f"命令执行失败: {' '.join(command) if isinstance(command, list) else command}")
            print_error(f"错误信息: {e.stderr if capture_output else str(e)}")
            return False
        except Exception as e:
            print_error(f"未知错误: {str(e)}")
            return False
        finally:
            command = old_command

    # todo: 专用函数推荐 _ 开头？
    def _is_git_repo(path):
        """检查目录是否是 Git 仓库"""
        git_dir = Path(path) / ".git"
        return git_dir.exists() and git_dir.is_dir()

    def setup_git():
        """初始化 Git 仓库并提交初始代码"""
        print_header("步骤 1: Git 初始化")

        if _is_git_repo("."):
            print_success("Git 仓库已存在，跳过初始化")
            return True

        print_step("初始化 Git 仓库")
        if not run_command(["git", "init"]):
            return False

        print_step("添加所有文件到暂存区")
        if not run_command(["git", "add", "."]):
            return False

        print_step("提交初始代码")
        if not run_command(["git", "commit", "-m", "initialize project"]):
            return False

        print_success("Git 初始化完成")
        return True

    def install_dependencies():
        """安装 Python 依赖"""
        print_header("步骤 2: 安装依赖")

        requirements_file = "requirements.txt"
        if not Path(requirements_file).exists():
            print_warning(f"{requirements_file} 文件不存在，跳过依赖安装")
            return True

        print_step("安装 Python 依赖")
        # todo: 此处的 pip 为什么正确？也确实使用了 requirements.txt，这意味着确实找到了这个文件啊。
        if run_command(["pip", "install", "-r", requirements_file], capture_output=True):
            print_success("依赖安装完成")
            return True
        return False

    def run_django_migrations():
        """执行 Django 迁移"""
        print_header("步骤 3: Django 数据库迁移")

        manage_py = "./backend/manager.py"
        # todo: 此处打印当前执行的工作目录
        print("当前工作目录（CWD）：", os.path.abspath("./"))
        print(Path(manage_py).resolve())
        # todo: FileNotFoundError: [Errno 2] No such file or directory: './backend/manager.py'
        #       这个文件明明存在啊？
        if not Path(manage_py).exists():
            print_error(f"{manage_py} 文件不存在，无法执行迁移")
            return False

        print_step("生成数据库迁移文件")

        if not run_command(["python", manage_py, "makemigrations"]):
            return False

        print_step("应用数据库迁移")
        if not run_command(["python", manage_py, "migrate"]):
            return False

        print_success("数据库迁移完成")
        return True

    def getpass_windows(prompt="密码: "):
        """替代方案（如果 getpass 不可用）"""
        print(prompt, end='', flush=True)
        password = []
        while True:
            print(123)
            ch = msvcrt.getch()
            print(ch)
            if ch == b'\r' or ch == b'\n\r':  # 回车键结束
                print()
                break
            password.append(ch.decode('utf-8'))
        return ''.join(password)

    def create_superuser():
        """创建 Django 超级用户"""
        print_header("步骤 4: 创建超级用户")

        manage_py = "./backend/manager.py"
        if not Path(manage_py).exists():
            print_error(f"{manage_py} 文件不存在，无法创建超级用户")
            return False

        print_step("检查 admin 用户是否已存在")
        check_user = run_command(
            ["python", manage_py, "shell", "-c",
             "from django.contrib.auth import get_user_model; "
             "User = get_user_model(); "
             "print(User.objects.filter(username='admin').exists())"],
            capture_output=True
        )

        if check_user and check_user.stdout.strip() == "True":
            print_success("admin 用户已存在，跳过创建")
            return True

        print_step("创建 admin 用户")

        # 获取用户输入
        print(f"{Colors.OKBLUE}请输入管理员信息:{Colors.ENDC}")
        # email = input("邮箱地址: ")

        # while True:
        #     password = getpass.getpass("密码: ")
        #     password_again = getpass.getpass("确认密码: ")
        #     if password == password_again:
        #         break
        #     print_error("两次输入的密码不一致，请重新输入")

        # fixme: 此处两种获得密码的方式都有问题，似乎一直等待输入？被阻塞？
        password = getpass_windows()

        # 创建用户命令
        command = [
            "python", manage_py, "createsuperuser",
            "--username", "admin",
            "--email", "django@example.com",
            "--noinput"
        ]

        # 启动进程
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 发送密码
        stdout, stderr = process.communicate(input=f"{password}\n{password}\n")

        if process.returncode != 0:
            print_error(f"创建超级用户失败: {stderr}")
            return False

        print_success("管理员账户创建成功")
        print(f"{Colors.OKGREEN}用户名: admin{Colors.ENDC}")
        return True

    def signal_handler(sig, frame):
        """处理 Ctrl+C 信号"""
        print("\n\n" + Colors.WARNING + "操作已被用户中断" + Colors.ENDC)
        sys.exit(1)

    if not Path(".").resolve().name == "your-project-name":  # 替换为实际项目名
        print_warning("注意: 请在项目根目录运行此脚本")

    # ------------------ 主函数 ------------------ #

    # todo: 好好参考一下此处 ai 生成的代码，很优雅的 POP（面向过程编程）

    # 定义需要执行的所有步骤
    steps = [
        ("初始化 Git 仓库并提交初始代码", setup_git),
        ("安装 Python 依赖", install_dependencies),
        ("执行 Django 数据库迁移", run_django_migrations),
        # ("创建超级用户", create_superuser),
    ]

    # 注册 Ctrl+C 信号处理
    signal.signal(signal.SIGINT, signal_handler)

    # 打印欢迎信息
    print_header("项目初始化自动化工具")
    print(f"{Colors.OKBLUE}此脚本将自动执行以下步骤:{Colors.ENDC}")
    for i in range(len(steps)):
        print(f"{i}. {steps[i][0]}")

    # 确认执行
    confirm = input(f"\n{Colors.WARNING}是否继续? (y/n): {Colors.ENDC}").strip().lower()
    if confirm != 'y':
        print("操作已取消")
        return

    start_time = time.time()

    all_success = True
    for name, func in steps:
        print_header(f"开始: {name}")
        if not func():
            print_error(f"{name} 步骤失败")
            all_success = False
            break

    # 显示结果
    print_header("初始化完成")
    elapsed_time = time.time() - start_time

    if all_success:
        print_success(f"所有步骤成功完成! 用时: {elapsed_time:.2f} 秒")
        print(f"\n{Colors.OKGREEN}项目已准备就绪，可以开始开发了！{Colors.ENDC}")
    else:
        print_error(f"初始化失败，部分步骤未完成。用时: {elapsed_time:.2f} 秒")
        print(f"\n{Colors.WARNING}请检查错误信息并手动完成剩余步骤。{Colors.ENDC}")

    # 显示后续步骤
    print("\n" + Colors.OKBLUE + "后续建议步骤:" + Colors.ENDC)
    print("- 启动开发服务器: " + Colors.BOLD + "python ./backend/manager.py runserver" + Colors.ENDC)
    print("- 运行测试: " + Colors.BOLD + "python ./backend/manager.py test" + Colors.ENDC)
    print("- 创建应用程序: " + Colors.BOLD + "python ./backend/manager.py startapp <app_name>" + Colors.ENDC)


if __name__ == '__main__':
    main()
