import os

from dotenv import load_dotenv
from loguru import logger

from nicegui import ui

content = {'Tab 1': 'Content 1', 'Tab 2': 'Content 2', 'Tab 3': 'Content 3'}
with ui.tabs() as tabs:
    for title in content:
        ui.tab(title)
with ui.tab_panels(tabs).classes('w-full') as panels:
    for title, text in content.items():
        with ui.tab_panel(title):
            ui.label(text)

ui.button('GoTo 1', on_click=lambda: panels.set_value('Tab 1'))
ui.button('GoTo 2', on_click=lambda: tabs.set_value('Tab 2'))

# ui.run()


ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
