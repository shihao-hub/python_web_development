from loguru import logger

from nicegui import ui
from fastapi.requests import Request


@ui.page('/icon/{icon}')
def icons(request: Request, icon: str, amount: int = 1):
    # request 可以访问主体负载、标头、cookie
    # todo: fastapi！需要进一步入门了解！
    logger.debug("{}", request)
    ui.label(icon).classes('text-h3')
    with ui.row():
        [ui.icon(icon).classes('text-h3') for _ in range(amount)]


ui.link('Star', '/icon/star?amount=5')
ui.link('Home', '/icon/home')
ui.link('Water', '/icon/water_drop?amount=3')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
