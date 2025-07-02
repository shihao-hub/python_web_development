from nicegui import ui

from frontend.settings import TITLE, HOST, PORT, SECRET_KEY

from pages import home, login  # todo: 确定一下，pages 代码执行怎么合理的执行，单纯导入似乎不合理

if __name__ == '__main__':
    # 实际上启动了 FastAPI 服务器
    ui.run(title=TITLE, host=HOST, port=PORT, reload=False, show=False, favicon="🚀", storage_secret=SECRET_KEY)
