import os
from typing import Optional

from loguru import logger

import re
from nicegui import ui

pwd = ui.input('Password', password=True, on_change=lambda: show_info.refresh())

rules = {
    'Lowercase letter': lambda s: re.search(r'[a-z]', s),
    'Uppercase letter': lambda s: re.search(r'[A-Z]', s),
    'Digit': lambda s: re.search(r'\d', s),
    'Special character': lambda s: re.search(r"[!@#$%^&*(),.?':{}|<>]", s),
    'min. 8 characters': lambda s: len(s) >= 8,
}


# [note] ui.refreshable 的 refresh 函数就是直接 clear 然后重新创建的...
@ui.refreshable
def show_info():
    for rule, check in rules.items():
        logger.debug("{} - {}", rule, check)
        with ui.row().classes('items-center gap-2'):
            if check(pwd.value or ''):
                ui.icon('done', color='green')
                ui.label(rule).classes('text-xs text-green strike-through')
            else:
                ui.icon('radio_button_unchecked', color='red')
                ui.label(rule).classes('text-xs text-red')


show_info()

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
