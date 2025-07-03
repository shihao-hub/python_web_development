"""
链接：https://gitee.com/carson_add/ex4nicegui



"""

from nicegui import ui
from ex4nicegui import rxui

from ex4nicegui import rxui, effect_refreshable


class AppState(rxui.ViewModel):
    icons = []
    _option_icons = ["font_download", "warning", "format_size", "print"]


state = AppState()

# 界面代码
with ui.row(align_items="center"):
    @effect_refreshable.on(state.icons)
    def _():
        for icon in state.icons:
            ui.icon(icon, size="2rem")

rxui.select(state._option_icons, value=state.icons, multiple=True)

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
