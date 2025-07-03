from loguru import logger

from nicegui import ui

editor = ui.editor(placeholder='Type something here')
ui.markdown().bind_content_from(editor, 'value',
                                backward=lambda v: f'HTML code:\n```\n{v}\n```')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123", on_air=True)
