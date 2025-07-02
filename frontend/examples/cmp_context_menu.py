from loguru import logger

from nicegui import ui

with ui.image('https://picsum.photos/id/377/640/360'):
    # [note] 右键展示
    with ui.context_menu():
        ui.menu_item('Flip horizontally')
        ui.menu_item('Flip vertically')
        ui.separator()
        ui.menu_item('Reset')

# ui.run()
ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
