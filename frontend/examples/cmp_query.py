from loguru import logger

from nicegui import ui


def set_background(color: str) -> None:
    # selector
    ui.query('body').style(f'background-color: {color}')


ui.button('Blue', on_click=lambda: set_background('#ddeeff'))
ui.button('Orange', on_click=lambda: set_background('#ffeedd'))

# 设置背景渐变、图像或类似效果非常简单
# 有关使用 CSS 设置背景的更多信息，请参见：https://www.w3schools.com/cssref/pr_background-image.php
# ui.query('body').classes('bg-gradient-to-t from-blue-400 to-blue-100')

# 默认情况下，NiceGUI 在页面内容周围提供了一个内置的内边距。您可以使用类选择器 .nicegui-content 来修改它。
ui.query('.nicegui-content').classes('p-0')
with ui.column().classes('h-screen w-full bg-gray-400 justify-between'):
    ui.label('top left')
    ui.label('bottom right').classes('self-end')

ui.button('Default', on_click=lambda: ui.colors())
ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))

# ui.radio(['x', 'y', 'z'], value='x').props('inline color=green', remove="", replace="") # 没有 replace
# ui.button(icon='touch_app').props('outline round').classes('shadow-lg', remove="", replace="")
# ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300', remove="", replace="")

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
