import os

from dotenv import load_dotenv

from nicegui import ui, app

import settings
from djangoorm import load_djangoorm

load_dotenv()
load_djangoorm()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoorm.djangoorm.settings")

app.add_static_files("/static", settings.STATIC_DIR)
app.add_media_files("/media", settings.MEDIA_DIR)


class Constants:
    pass


class Service:
    pass


class View:
    def __init__(self):
        self._create_header()
        self._create_left_drawer()
        self._create_content()

    def _create_header(self):
        # todo: 确定一下 tailwind 联想真的好用吗？难道是纯前端好用？
        with ui.header().classes("w-full bg-blue-300"):
            with ui.label("饥荒后台").classes("w-1/6"):
                ui.link()  # todo: 点击选中工具栏第一个
            with ui.row().classes("flex justify-between"):
                with ui.button(icon="menu"):
                    with ui.menu():
                        pass
                with ui.row():
                    ui.button("放大")  # todo: 有个放大缩小图标
                    with ui.button(icon="menu"):
                        with ui.menu() as menu:
                            pass

    def _create_left_drawer(self):
        with ui.left_drawer():
            with ui.grid(columns=1):
                with ui.row():
                    ui.icon("home")
                    ui.label("管理员")
            ui.button("控制台")
            ui.button("房间设置")
            ui.button("玩家管理")
            ui.button("备份管理")
            ui.button("帮助文档")
            ui.button("系统设置")
            ui.button("关于")

    def _create_content(self):
        pass


@ui.page("/")
def page_index():
    View()


if __name__ == '__main__':
    ui.run(title=settings.TITLE,
           favicon=settings.FAVICON,
           host=settings.HOST,
           port=settings.PORT,
           reload=False,
           show=False,
           on_air=os.getenv("NICEGUI_TOKEN"),
           storage_secret="NOSET")
