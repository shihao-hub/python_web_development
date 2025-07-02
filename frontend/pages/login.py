from loguru import logger

from nicegui import ui, app
from nicegui.client import Client

# 用户数据库
users = {'user1': 'pass1', 'user2': 'pass2', "admin": "django123456"}


@ui.page('/login')
def login():
    def try_login():
        # todo: 自己实现一个原始的登录逻辑？话说不行吧，没有 https 的话？
        #       必须自己实现一个，哪怕最原始！所以第一件事我应该是去了解一下原理，如何实现一套原始的登录系统！
        if username.value in users and users[username.value] == password.value:
            # 记录用户登录状态
            # todo: [to be understood] 这个修改是修改了前端的 session 吗？
            # fixme: 不对，这个 client_id 不对，每次都是新的，我真服了！nicegui 改动很大吗？ai 很多错误啊！
            # 使用 @ui.page 装饰器创建的页面是 私有 的。它们的内容会为每个客户端重新创建。
            # 因此，当浏览器重新加载页面时，私人页面上显示的 ID 会发生变化。
            # 注意，是每次刷新！所以不能用这个，就是需要去了解一下最原始的登录系统！用到了浏览器的哪些内容！
            # 2025-07-03：这时候体现出来理论知识的重要性了，ai 错误非常多的情况下，博客知识还是很重要的！
            client_id = ui.context.client.id
            logger.debug("/login client_id: {}", client_id)
            app.storage.user[client_id] = {'username': username.value}
            ui.navigate.to('/home')
            error_label.set_visibility(False)
        else:
            error_label.set_visibility(True)

    username = ui.input('Username')
    password = ui.input('Password', password=True)
    ui.button('Login', on_click=try_login)
    error_label = ui.label('Invalid credentials!').style("color: red;")
    error_label.set_visibility(False)

    username.on("input", lambda: error_label.set_visibility(False))
    password.on("input", lambda: error_label.set_visibility(False))
