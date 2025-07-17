from nicegui import ui

with ui.element("div").classes("mx-auto"):
    with ui.element("div").classes("flex mx-auto"):
        title = ui.label("任务列表")
        title.tailwind.font_size("2xl").font_weight("bold")
    with ui.column():
        ui.label("1")
        ui.label("2")
        ui.label("3")

ui.run(show=False, reload=False)
