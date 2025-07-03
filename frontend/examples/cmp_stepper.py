import os
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

from nicegui import ui

extra: Optional[ui.step] = None


@ui.refreshable
def create_extra_step():
    with stepper:
        global extra
        extra = ui.step('extra')
        with extra:
            ui.label('Extra')
            with ui.stepper_navigation():
                ui.button('Back', on_click=stepper.previous).props('flat')
                ui.button('Next', on_click=stepper.next)
        extra.move(target_index=1)


def next_step() -> None:
    if extra_step.value and len(stepper.default_slot.children) == 2:
        if not hasattr(create_extra_step, "_gt_one"):
            create_extra_step()
            setattr(create_extra_step, "_gt_one", True)
        else:
            create_extra_step.refresh()
    stepper.next()


# todo: horizontal 如何？
with ui.stepper().props('vertical').classes('w-full') as stepper:
    with ui.step('start'):
        ui.label('Start')


        def handle_change(e):
            extra.set_visibility(e)


        extra_step = ui.checkbox('do extra step', on_change=handle_change)
        # todo: 绑定 checkbox 的 visibility？
        extra_step.bind_visibility(extra_step)

        with ui.stepper_navigation():
            ui.button('Next', on_click=next_step)
    with ui.step('finish'):
        ui.label('Finish')
        with ui.stepper_navigation():
            ui.button('Back', on_click=stepper.previous).props('flat')

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
