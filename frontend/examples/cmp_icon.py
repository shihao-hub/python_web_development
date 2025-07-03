from nicegui import ui

with ui.row().classes('text-4xl'):
    ui.icon('home')
    ui.icon('o_home')
    ui.icon('r_home')
    ui.icon('sym_o_home')
    ui.icon('sym_r_home')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
