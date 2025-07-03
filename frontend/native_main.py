"""
[原生模式](https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/Config/native.html)

"""

from nicegui import native

from main import run

if __name__ == '__main__':
    run(port=native.find_open_port(), native_option=True)
