import os
from typing import Optional

from loguru import logger

from nicegui import ui
from nicegui.events import KeyEventArguments


def handle_key(e: KeyEventArguments):
    if e.key == 'f' and not e.action.repeat:
        if e.action.keyup:
            ui.notify('f was just released')
        elif e.action.keydown:
            ui.notify('f was just pressed')

    # todo: 注意，键盘监听，两个键依次按下，第一次按下不松开是不是事件一直触发啊？第二次再按就触发到了
    # logger.debug("{}, {}, {}", e, e.modifiers, e.action)
    # answer: 似乎确实如此！这就是 e.action.repeat 判断条件的作用了
    if e.modifiers.shift and e.action.keydown:
        if e.key.arrow_left:
            ui.notify('going left')
        elif e.key.arrow_right:
            ui.notify('going right')
        elif e.key.arrow_up:
            ui.notify('going up')
        elif e.key.arrow_down:
            ui.notify('going down')


keyboard = ui.keyboard(on_key=handle_key)
ui.label('Key events can be caught globally by using the keyboard element.')
ui.checkbox('Track key events').bind_value_to(keyboard, 'active')

# ui.run()


ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
