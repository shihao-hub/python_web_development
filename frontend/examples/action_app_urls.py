
from nicegui import app, ui

@ui.page('/')
def index():
    for url in app.urls:
        ui.link(url, target=url)

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="&#128640;", storage_secret="123")



