import os
from typing import Optional

import asyncio
from nicegui import ui


# 注意：您还可以将 functools.partial 传递给 on_click 属性，以包装带参数的异步函数。
# 在我目前的理解看来，就是等价于传递了传递了闭包起来的 upvalues（Python 不同于 Lua，Python 的闭包是那个变量的引用，而且会变）

async def async_task():
    ui.notify('Asynchronous task started')
    await asyncio.sleep(5)
    ui.notify('Asynchronous task finished')


ui.button('start async task', on_click=async_task)

# ui.run()

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
