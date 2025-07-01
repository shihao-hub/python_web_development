from nicegui import ui

ui.html('This is <strong>HTML</strong>.', tag="h1")

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀")
