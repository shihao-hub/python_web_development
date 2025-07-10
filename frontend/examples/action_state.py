import os
from typing import Optional

from nicegui import ui

@ui.refreshable
def counter(name: str):
    with ui.card():
        # todo: 确定一下，这是 react 的内容吧？{} 与 set_{}
        count, set_count = ui.state(0)
        color, set_color = ui.state('black')
        ui.label(f'{name} = {count}').classes(f'text-{color}')
        ui.button(f'{name} += 1', on_click=lambda: set_count(count + 1))
        ui.select(['black', 'red', 'green', 'blue'],
                  value=color, on_change=lambda e: set_color(e.value))

with ui.row():
    counter('A')
    counter('B')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
