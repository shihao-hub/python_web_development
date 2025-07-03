from loguru import logger

from nicegui import ui


@ui.page("/")
def page():
    json = {
        'Name': 'Alice',
        'Age': 42,
        'Address': {
            'Street': 'Main Street',
            'City': 'Wonderland',
        },
    }
    editor = ui.json_editor({'content': {'json': json}})

    ui.button('Expand', on_click=lambda: editor.run_editor_method(':expand', 'path => true'))
    ui.button('Collapse', on_click=lambda: editor.run_editor_method(':expand', 'path => false'))
    ui.button('Readonly', on_click=lambda: editor.run_editor_method('updateProps', {'readOnly': True}))
    ui.button('NotReadonly', on_click=lambda: editor.run_editor_method('updateProps', {'readOnly': False}))

    async def get_data() -> None:
        data = await editor.run_editor_method('get')
        ui.notify(data)

    ui.button('Get Data', on_click=get_data)


# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123", on_air=True)
