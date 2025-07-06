import os
from typing import Optional


from nicegui import ui

with ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):
    badge = ui.badge('0', color='red').props('floating')

# ui.run()


ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
