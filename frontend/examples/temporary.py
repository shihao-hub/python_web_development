from loguru import logger

from nicegui import ui
from uuid import uuid4


@ui.page('/private_page')
async def private_page():
    ui.label(f'private page with ID {uuid4()}')


ui.label(f'shared auto-index page with ID {uuid4()}')
ui.link('private page', private_page)

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
