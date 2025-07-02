from loguru import logger

from nicegui import app, ui


@ui.page('/')
def index():
    ui.textarea('This note is kept between visits').classes('w-full').bind_value(app.storage.user, 'note')


# todo: 弄清楚，目前的现象是，同一个浏览器之间访问 / 都算是同一个用户，但是不同浏览器就不是了。
# todo: .nicegui 中使用 .json 充当 app.storage.user 存储体，而且我发现这个命名也挺有意思的，视为 . 替换为 -
# todo: 弄清楚，这么多文件？难道不会定期清理吗？不对劲啊。

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
