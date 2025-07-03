from loguru import logger

from nicegui import ui

t = ui.tree([
    {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}], 'disabled': True},
    {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},
], label_key='id').expand()

with ui.row():
    ui.button('+ all', on_click=t.expand)
    ui.button('- all', on_click=t.collapse)
    ui.button('+ A', on_click=lambda: t.expand(['A']))
    ui.button('- A', on_click=lambda: t.collapse(['A']))

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123", on_air=True)
