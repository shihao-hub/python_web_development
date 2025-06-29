import datetime
import sqlite3
from typing import List, Tuple, Dict, Any, Optional

from loguru import logger

from nicegui import ui

connect = sqlite3.connect("./db.sqlite3")

# sqlite: NULL, INTERGE, REAL, TEXT, BLOB
connect.execute("""
CREATE TABLE IF NOT EXISTS todolist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    category TEXT NOT NULL,
    due_date TEXT
);
""")
connect.commit()


class TodoDB:
    """封装数据库操作"""
    TABLE_NAME = "todolist"
    COLUMNS = ("id", "text", "completed", "category", "due_date")

    @staticmethod
    def execute_query(query: str, params: tuple = ()) -> List[tuple]:
        """执行查询并返回结果"""
        cursor = connect.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    @staticmethod
    def execute_update(query: str, params: tuple = ()):
        """执行更新操作并提交事务"""
        cursor = connect.cursor()
        cursor.execute(query, params)
        connect.commit()

    @classmethod
    def get_all_todos(cls) -> List[Dict[str, Any]]:
        """获取所有待办事项"""
        results = cls.execute_query(f"SELECT * FROM {cls.TABLE_NAME}")
        todos = []
        for row in results:
            # 进行数据转换
            todo = dict(zip(cls.COLUMNS, row))
            todo['completed'] = bool(todo['completed'])
            todos.append(todo)
        logger.debug("获取的代办事项的数量：{}", len(todos))
        return todos

    @classmethod
    def add_todo(cls, text: str, category: str, due_date: Optional[str] = None) -> int:
        """添加新待办事项，返回新ID"""
        cls.execute_update(
            f"INSERT INTO {cls.TABLE_NAME} (text, category, due_date) VALUES (?, ?, ?)",
            (text, category, due_date)
        )
        # 获取最后插入的ID
        cursor = connect.cursor()
        cursor.execute("SELECT last_insert_rowid()")
        return cursor.fetchone()[0]

    @classmethod
    def toggle_todo(cls, todo_id: int):
        """切换待办事项完成状态"""
        cls.execute_update(
            f"UPDATE {cls.TABLE_NAME} SET completed = NOT completed WHERE id = ?",
            (todo_id,)
        )

    @classmethod
    def delete_todo(cls, todo_id: int):
        """删除待办事项"""
        cls.execute_update(
            f"DELETE FROM {cls.TABLE_NAME} WHERE id = ?",
            (todo_id,)
        )

    @classmethod
    def update_todo(cls, todo_id: int, text: str, category: str, due_date: Optional[str] = None):
        """更新待办事项"""
        cls.execute_update(
            f"UPDATE {cls.TABLE_NAME} SET text = ?, category = ?, due_date = ? WHERE id = ?",
            (text, category, due_date, todo_id)
        )


class TodoViewModel:
    def __init__(self):
        self.todo_listeners = []
        self.stats_listeners = []

    def on_todo_change(self, callback):
        self.todo_listeners.append(callback)

    def on_stats_change(self, callback):
        self.stats_listeners.append(callback)

    def notify_todos_changed(self):
        for cb in self.todo_listeners:
            cb()

    def notify_stats_changed(self):
        for cb in self.stats_listeners:
            cb()


# 实例化
view_model = TodoViewModel()


# 待办事项管理类
class TodoApp:
    def __init__(self):
        self.todos = []
        self.categories = ['工作', '个人', '购物', '学习']
        self.filter = '全部'
        self.todos = self.load_todos()

    def load_todos(self):
        """从数据库加载所有待办事项"""
        logger.debug("从数据库加载待办事项")
        return TodoDB.get_all_todos()

    def add_todo(self, text, category, due_date=None):
        if not text:
            ui.notify('请输入待办事项内容', type='warning')
            return

        TodoDB.add_todo(text, category, due_date)
        # 重新加载数据
        self.todos = self.load_todos()

        ui.notify(f'已添加: {text}', type='positive')
        # todo: model 触发 view 刷新
        view_model.notify_todos_changed()
        view_model.notify_stats_changed()

    def toggle_todo(self, todo_id):
        """切换待办事项完成状态"""
        logger.info("toggle_todo")
        TodoDB.toggle_todo(todo_id)
        # 重新加载数据
        self.todos = self.load_todos()

        view_model.notify_todos_changed()
        view_model.notify_stats_changed()

    def delete_todo(self, todo_id):
        """删除待办事项"""
        TodoDB.delete_todo(todo_id)
        # 重新加载数据
        self.todos = self.load_todos()

        ui.notify('待办事项已删除', type='info')
        view_model.notify_todos_changed()
        view_model.notify_stats_changed()

    def update_todo(self, todo_id: int, text: str, category: str, due_date: Optional[str] = None):
        """更新待办事项"""
        TodoDB.update_todo(todo_id, text, category, due_date)
        self.todos = self.load_todos()  # 重新加载数据

        ui.notify(f'已更新: {text}', type='positive')
        view_model.notify_todos_changed()
        view_model.notify_stats_changed()

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


# 绑定刷新函数
view_model.on_todo_change(refresh_todolist_widget.refresh)
view_model.on_stats_change(refresh_statistics_widget.refresh)


def todolist_tab_panel(tab):
    # 待办事项面板
    # [note] bg-blue-200 修改了背景颜色，更方便初学者判断元素位置
    # [note] mx-auto max-w-[50%] bg-blue-200 p-4 这个 classes 让我做到了居中显示，css 的原理需要了解啊
    # fixme: 这个 max-w-[50%] 似乎固定了宽度，不同分辨率的情况下，有差异啊。。
    with ui.tab_panel(tab).classes("mx-auto max-w-[60%] bg-blue-200 p-4") as todo_section:
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
