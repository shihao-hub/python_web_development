from collections import Counter
from datetime import datetime

from loguru import logger

from nicegui import app, ui

counter = Counter()
start = datetime.now().strftime('%H:%M, %d %B %Y')


@ui.page('/')
def index():
    # [note] 测试发现，app.storage.browser['id'] 用于识别用户（同一浏览器未清除 session 的话，id 不变）
    #        counter，start 似乎是不同 page 间共享的
    #        注意，F5 每次刷新的时候，似乎都是个新 page
    logger.debug("app.storage.browser['id']: {}", app.storage.browser['id'])
    counter[app.storage.browser['id']] += 1
    ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')


@ui.page('/2')
def index2():
    """存储 ui 状态，与绑定结合使用，同一用户的所有标签页之间也共享该便签"""
    ui.textarea('This note is kept between visits') \
        .classes('w-full').bind_value(app.storage.user, 'note')

# ui.run(storage_secret='private key to secure the browser session cookie')


ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
