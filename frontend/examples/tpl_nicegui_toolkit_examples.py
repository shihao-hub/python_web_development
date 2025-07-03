from loguru import logger

from nicegui import ui

from nicegui_toolkit.layout_tool import inject_layout_tool

# todo: 源码值得阅读
inject_layout_tool(ide="pycharm", language_locale="zh")

with ui.column():
    with ui.column():
        with ui.row():
            ui.label('username:').classes("mt-10")
            ui.input()

        with ui.row():
            ui.label('password:').classes("mt-10")
            ui.input()

    with ui.grid(columns=2):
        ui.button('Register', icon="person_add")
        ui.button('Login', icon="login")

# ui.run()

# todo: native=True
ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
