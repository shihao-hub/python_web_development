from datetime import datetime
from nicegui import app, ui

dt = datetime.now()


def handle_connection():
    global dt
    dt = datetime.now()


app.on_connect(handle_connection)

label = ui.label()
ui.timer(1, lambda: label.set_text(f'Last new connection: {dt:%H:%M:%S}'))

# ui.run()

# app.on_exception：发生异常时调用（可选参数：exception）

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
