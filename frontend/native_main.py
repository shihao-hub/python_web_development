"""
[原生模式](https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/Config/native.html)

"""
import os

from dotenv import load_dotenv

from nicegui import native

from main import run

load_dotenv()

if __name__ == '__main__':
    # native.find_open_port()
    run(port=12000, native_option=True, on_air=os.getenv("NICEGUI_TOKEN"))
