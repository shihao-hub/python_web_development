import datetime

import pytz

from nicegui import ui

from tabpanels.todolist import todolist_tab_panel
from tabpanels.weather_query import weather_query_panel
from tabpanels.about import about_panel

# todo: 放入配置文件中读取，或者修改 sources root？

TITLE = "待办事项和天气查询"


def ui_open(url):
    ui.run_javascript(f"window.open('{url}', '_blank')")


# 设置页面布局
with ui.header().classes('bg-blue-500 text-white justify-between'):
    ui.label(f'{TITLE}').classes('text-2xl font-bold')
    # with ui.row():
    #     ui.button('待办事项', on_click=lambda: ui_open('#todo-section'))
    #     ui.button('天气查询', on_click=lambda: ui_open('#weather-section'))
    #     ui.button('关于', on_click=lambda: ui_open('#about-section'))
    #     ui.button(icon='dark_mode', on_click=ui.dark_mode.toggle).props('flat')

# 主内容区域
with ui.tabs().classes('w-full') as tabs:
    todo_tab = ui.tab('待办事项', icon='list')
    weather_tab = ui.tab('天气查询', icon='cloud')
    about_tab = ui.tab('关于', icon='info')

with ui.tab_panels(tabs, value=todo_tab).classes('w-full'):
    todolist_tab_panel(todo_tab)
    weather_query_panel(weather_tab)
    about_panel(about_tab)

# 页脚
with ui.footer().classes('bg-blue-500 dark:bg-gray-800 p-4 text-center'):
    with ui.row():
        ui.label(f'© 2025 {TITLE}')
        current_time = ui.label()


        def update_current_time():
            current_time_str = datetime.datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
            current_time.text = f"当前时间: {current_time_str}"


        ui.timer(1.0, update_current_time)

# 启动应用
ui.run(title=TITLE, host="localhost", port=13002, favicon='🌤️', dark=False, show=False, reload=False)
