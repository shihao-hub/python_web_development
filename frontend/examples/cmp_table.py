import os
from typing import Optional

from nicegui import ui

columns = [
    {'name': 'name', 'label': 'Name', 'field': 'name'},
    {'name': 'age', 'label': 'Age', 'field': 'age'},
]
rows = [
    {'name': 'Alice', 'age': 42},
    {'name': 'Bob', 'age': 23},
]
ui.table(columns=columns, rows=rows, row_key='name').on('rowClick', lambda e: (
    ui.notify(f'You clicked on {e.args}')
), [[], ['name'], None])  # todo: 此处想表达的是，点击把表格的属性/值传递过来做一些处理？

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
