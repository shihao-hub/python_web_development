import re

from loguru import logger

from nicegui import events, ui

with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()


def handle_upload(e: events.UploadEventArguments):
    text = e.content.read().decode('utf-8')
    content.set_content(text)
    dialog.open()


ui.upload(on_upload=handle_upload).props('accept=.md').classes('max-w-full')

# ui.run()


ui.run(host="localhost", port=15000, reload=False, show=False, favicon="🚀")
