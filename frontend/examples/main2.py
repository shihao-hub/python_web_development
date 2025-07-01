from dataclasses import dataclass, field
from typing import Callable, List

from nicegui import ui


@dataclass
class TodoItem:
    name: str
    done: bool = False


@dataclass
class ToDoList:
    title: str
    on_change: Callable
    items: List[TodoItem] = field(default_factory=list)

    def add(self, name: str, done: bool = False) -> None:
        self.items.append(TodoItem(name, done))
        self.on_change()

    def remove(self, item: TodoItem) -> None:
        self.items.remove(item)
        self.on_change()


@ui.refreshable
def todo_ui():
    if not todos.items:
        ui.label('List is empty.').classes('mx-auto')
        return
    ui.linear_progress(sum(item.done for item in todos.items) / len(todos.items), show_value=False)
    with ui.row().classes('justify-center w-full'):
        ui.label(f'Completed: {sum(item.done for item in todos.items)}')
        ui.label(f'Remaining: {sum(not item.done for item in todos.items)}')
    for item in todos.items:
        with ui.row().classes('items-center'):
            ui.checkbox(value=item.done, on_change=todo_ui.refresh).bind_value(item, 'done')
            ui.input(value=item.name).classes('flex-grow').bind_value(item, 'name')
            ui.button(on_click=lambda e=item: todos.remove(e), icon='delete').props('flat fab-mini color=grey')


todos = ToDoList('My Weekend', on_change=todo_ui.refresh)
todos.add('Order pizza', done=True)
todos.add('New NiceGUI Release')
todos.add('Clean the house')
todos.add('Call mom')

with ui.card().classes('w-80 items-stretch'):
    ui.label().bind_text_from(todos, 'title').classes('text-semibold text-2xl')
    todo_ui()
    add_input = ui.input('New item').classes('mx-12')
    add_input.on('keydown.enter', lambda: (todos.add(add_input.value), add_input.set_value('')))

ui.run()

"""
todo:
1. https://juejin.cn/post/7289297739535663143
nicegui 基于 Python 编程语言开发，采用了声明式的方式来描述用户界面。
它的设计灵感来自于 Web 开发中的 HTML 和 CSS，通过一种类似的结构化语法来描述界面的组件和样式。
nicegui 的核心思想是将用户界面分为多个组件，每个组件具有自己的属性和样式。
开发者可以使用 nicegui 提供的组件库，如按钮、文本框、下拉菜单等，通过简单的代码来定义和布局这些组件。
同时，nicegui 还支持自定义组件，开发者可以根据自己的需求扩展组件库。

=> 需要使用前端的编程风格来编写 nicegui 代码，比如 getElementById、.on .emit 等

2. https://juejin.cn/post/7247901054238179365?from=search-suggest

3. https://juejin.cn/post/7425528033971224615?from=search-suggest

4. https://juejin.cn/post/7314485430385180712?from=search-suggest

5. https://blog.csdn.net/zai_yuzhong/article/details/147380665

6. https://zhuanlan.zhihu.com/p/651940772

7. https://www.bing.com/search?pc=MOZI&form=MOZLBR&q=nicegui+%E5%8E%9F%E7%90%86%E5%89%96%E6%9E%90&ntref=1

8. https://www.cnblogs.com/larkwins/p/18182050

9. https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/intro.html

10. https://www.atyun.com/59283.html

"""
