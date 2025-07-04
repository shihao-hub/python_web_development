import os
from typing import Optional

from nicegui import ui

with ui.row().classes('items-center m-auto'):
    with ui.circular_progress(value=0.1, show_value=False) as progress:
        ui.button(
            icon='star',
            on_click=lambda: progress.set_value(progress.value + 0.1)
        ).props('flat round')
    ui.label('click to increase progress')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
