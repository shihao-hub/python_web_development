from typing import Union, Optional, Literal

from nicegui import ui, native

from nicegui_toolkit.layout_tool import inject_layout_tool

from frontend.settings import TITLE, HOST, PORT, SECRET_KEY

from pages import home, login  # todo: 确定一下，pages 代码执行怎么合理的执行，单纯导入似乎不合理


# todo: 它导致 button 无法点击了啊？难受！能解决吗？
# inject_layout_tool(ide="pycharm", language_locale="zh")


# temp
@ui.page("/")
def index_page():
    ui.navigate.to("/home")


def run(port: int = PORT, native_option: bool = False, on_air: Optional[Union[str, Literal[True]]] = None):
    # 实际上启动了 FastAPI 服务器
    ui.run(title=TITLE, host=HOST, port=port, reload=False, show=False, favicon="🚀", storage_secret=SECRET_KEY,
           native=native_option,on_air=on_air)


if __name__ == '__main__':
    run()
