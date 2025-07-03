from loguru import logger

from nicegui import ui

with ui.list().props('bordered separator'):
    ui.item_label('Contacts').props('header').classes('text-bold')
    ui.separator()
    with ui.item(on_click=lambda: ui.notify('Selected contact 1')):
        with ui.item_section().props('avatar'):
            ui.icon('person')
        with ui.item_section():
            ui.item_label('Nice Guy')
            ui.item_label('name').props('caption')
        with ui.item_section().props('side'):
            ui.icon('chat')
    with ui.item(on_click=lambda: ui.notify('Selected contact 2')):
        with ui.item_section().props('avatar'):
            ui.icon('person')
        with ui.item_section():
            ui.item_label('Nice Person')
            ui.item_label('name').props('caption')
        with ui.item_section().props('side'):
            ui.icon('chat')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
