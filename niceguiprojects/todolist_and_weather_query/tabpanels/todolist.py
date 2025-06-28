import datetime

from loguru import logger

from nicegui import ui


# 待办事项管理类
class TodoApp:
    def __init__(self):
        self.todos = []
        self.categories = ['工作', '个人', '购物', '学习']
        self.filter = '全部'
        self.load_todos()

    def load_todos(self):
        # 模拟加载一些初始数据
        self.todos = [
            {'id': 1, 'text': '学习 NiceGUI', 'completed': True, 'category': '学习', 'due_date': None},
            {'id': 2, 'text': '购买杂货', 'completed': False, 'category': '购物', 'due_date': None},
            {'id': 3, 'text': '完成项目报告', 'completed': False, 'category': '工作',
             'due_date': datetime.date.today().isoformat()},
        ]

    def add_todo(self, text, category, due_date=None):
        if not text:
            ui.notify('请输入待办事项内容', type='warning')
            return

        new_id = max([t['id'] for t in self.todos], default=0) + 1
        self.todos.append({
            'id': new_id,
            'text': text,
            'completed': False,
            'category': category,
            'due_date': due_date
        })
        self.save_todos()
        ui.notify(f'已添加: {text}', type='positive')
        # todo: model 触发 view 刷新
        refresh_todolist_widget.refresh()
        refresh_statistics_widget.refresh()

    def toggle_todo(self, todo_id):
        logger.info("toggle_todo")
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['completed'] = not todo['completed']
                break
        self.save_todos()
        refresh_todolist_widget.refresh()
        refresh_statistics_widget.refresh()

    def delete_todo(self, todo_id):
        self.todos = [t for t in self.todos if t['id'] != todo_id]
        self.save_todos()
        ui.notify('待办事项已删除', type='info')
        refresh_todolist_widget.refresh()
        refresh_statistics_widget.refresh()

    def save_todos(self):
        # 在实际应用中，这里会保存到数据库
        pass

    def filtered_todos(self):
        if self.filter == '全部':
            return self.todos
        elif self.filter == '已完成':
            return [t for t in self.todos if t['completed']]
        elif self.filter == '未完成':
            return [t for t in self.todos if not t['completed']]
        else:
            return [t for t in self.todos if t['category'] == self.filter]


# 创建应用实例
todo_app = TodoApp()


# todo: 了解 ui.refreshable 的原理，vue 的 reactive？好强。
@ui.refreshable
def refresh_todolist_widget():
    with ui.column().classes('w-full gap-2'):
        for todo in todo_app.filtered_todos():
            with ui.card().classes('w-full p-3').style('opacity: 0.8' if todo['completed'] else ''):
                with ui.row().classes('items-center'):

                    ui.checkbox(value=todo['completed'],
                                on_change=lambda e, _id=todo['id']: todo_app.toggle_todo(_id))
                    # [note] 此处进行了双向绑定，on_change 中修改 todo["completed"] 的同时，再次触发了此处...
                    # .bind_value(todo, 'completed')

                    ui.label(todo['text']).classes('ml-2 flex-grow').style(
                        'text-decoration: line-through' if todo['completed'] else '')

                    if todo['category']:
                        ui.badge(todo['category'], color={
                            '工作': 'blue',
                            '个人': 'green',
                            '购物': 'purple',
                            '学习': 'orange'
                        }.get(todo['category'], 'grey'))

                    if todo['due_date']:
                        due_date = datetime.date.fromisoformat(todo['due_date'])
                        days_left = (due_date - datetime.date.today()).days
                        badge_color = 'red' if days_left < 0 else 'orange' if days_left == 0 else 'blue'
                        ui.badge(f'截止: {todo["due_date"]} ({days_left}天)', color=badge_color).classes('ml-2')

                    ui.button(icon='delete', on_click=lambda _, id=todo['id']: todo_app.delete_todo(id)) \
                        .props('flat dense').classes('ml-2')


@ui.refreshable
def refresh_statistics_widget():
    with ui.row().classes('w-full justify-between mt-4'):
        completed = sum(1 for t in todo_app.todos if t['completed'])
        total = len(todo_app.todos)
        ui.label(f'完成: {completed}/{total} ({int(completed / total * 100) if total else 0}%)')
        ui.linear_progress(value=completed / total if total else 0).classes('w-1/3')


def todolist_tab_panel(tab):
    # 待办事项面板
    # [note] bg-blue-200 修改了背景颜色，更方便初学者判断元素位置
    # [note] mx-auto max-w-[50%] bg-blue-200 p-4 这个 classes 让我做到了居中显示，css 的原理需要了解啊
    with ui.tab_panel(tab).classes("mx-auto max-w-[50%] bg-blue-200 p-4") as todo_section:
        # [warning] 这里错了居然没有提示，整个页面出了问题
        # todo_section.id = 'todo-section'

        with ui.row().classes('w-full items-center'):
            ui.label('待办事项管理').classes('text-xl font-bold')
            ui.space()
            with ui.select(options=['全部', '已完成', '未完成'] + todo_app.categories,
                           value='全部', on_change=lambda e: refresh_todolist_widget.refresh()) \
                    .bind_value(todo_app, 'filter').classes('w-40'):
                ui.tooltip('过滤待办事项')

        # 添加新待办事项的表单
        with ui.card().classes('w-full p-4 mb-4'):
            with ui.row().classes('w-full items-center'):
                task_input = ui.input(placeholder='输入新的待办事项...').classes('flex-grow')
                category_select = ui.select(options=todo_app.categories, value='工作').classes('w-32')
                # todo: 将其缩小，选中弹出来？或者改成水平？
                date_input = ui.date(value=datetime.date.today().isoformat()).classes('w-40')
                ui.button('添加', icon='add', on_click=lambda: todo_app.add_todo(
                    task_input.value,
                    category_select.value,
                    date_input.value
                )).classes('ml-2')

        # 待办事项列表:todolist_widget
        refresh_todolist_widget()

        # 统计信息:statistics_widget
        refresh_statistics_widget()
