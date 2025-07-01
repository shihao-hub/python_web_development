from dataclasses import dataclass
from typing import List
from functools import partial  # for 循环中可以通过它解决闭包陷阱

from loguru import logger

from nicegui import ui

DEFAULT_IMAGE = ""


@dataclass
class CodeInfo:
    code: str
    image: str


code_infos: List[CodeInfo] = []

# todo: 熟悉 Tailwind 类，以美化页面（皮肤）


# 构建骨架（on_click 等回调应该算是血肉，此时体现出面向对象的好处 self.x = y）
with ui.row() as add_panel:
    code_input = ui.input(placeholder="请输入 nicegui 代码")
    ui.button('新增', on_click=lambda: (
        code_infos.append(CodeInfo(code=code_input.value, image=DEFAULT_IMAGE)),
        create_show_panel.refresh()
    ))

ui.element("hr")


@ui.refreshable
def create_show_panel():
    with ui.column() as show_panel:
        for code_info in code_infos:
            with ui.card() as card:
                with ui.row():
                    ui.markdown(code_info.code)
                    ui.image(code_info.image)

                # todo: 确定一下 on_click 是否可以不止放在此处
                def make_on_click(code_info):
                    def cb():
                        try:
                            # todo: 应该启动一个子进程，随机选择端口，运行后用自动化技术进行截图
                            #       此时发现，需求未来到底有没有用，也是个关键，否则白费功夫
                            result = eval(code_info.code)
                            ui.notify(f"success, result: {result}", type='positive')
                        except Exception as e:
                            logger.error(e)
                            ui.notify(e, type='negative')

                    return cb

                with ui.row():
                    render_btn = ui.button('渲染', on_click=make_on_click(code_info))

                    # [note] partial 解决了闭包陷阱，固定了参数值，对于返回的函数来说，请将被固定的参数单纯视为 upvalue
                    ui.button('删除', on_click=partial(
                        lambda code_info, card: (
                            code_infos.remove(code_info),
                            card.delete(),
                            show_panel.update()
                        ),
                        code_info,
                        card
                    ))


create_show_panel()

ui.run(host="localhost", port=15000, reload=False, show=False, favicon="🚀")
