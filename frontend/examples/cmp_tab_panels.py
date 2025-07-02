from loguru import logger

from nicegui import ui, events

# 存储标签页内容的容器字典，key 为标签名，value 为对应的内容容器
tab_containers = {}

tabs = ui.tabs().classes('w-full')
with tabs:
    tab1 = ui.tab('tab1')
    tab2 = ui.tab('tab2')
    tab3 = ui.tab('tab3')

# 内容区域
content_container = ui.column().classes('w-full')


def create_tab_content(tab_name):
    """创建标签页内容并存储在容器中"""
    if tab_name in tab_containers:
        return tab_containers[tab_name]

    # 创建一个列容器来放置内容，并设置可见性
    with ui.column().classes('w-full') as container:
        # 这里创建标签页的具体内容
        if tab_name == 'tab1':
            ui.label('Content for Tab 1')
            slider = ui.slider(min=0, max=100, value=50)
            # 可以添加更多元素
        elif tab_name == 'tab2':
            ui.label('Content for Tab 2')
            checkbox = ui.checkbox('Check me')
        elif tab_name == 'tab3':
            ui.label('Content for Tab 3')
            input = ui.input('Enter something')

    # 初始时隐藏
    container.set_visibility(False)
    tab_containers[tab_name] = container
    return container


def handle_tab_change(e: events.GenericEventArguments):
    logger.info("call handle_tab_change")
    # 隐藏所有内容
    for container in tab_containers.values():
        container.set_visibility(False)

    logger.debug("{}", e.args)

    # 显示当前选中的标签页内容
    if e.args in tab_containers:
        tab_containers[e.args].set_visibility(True)
    else:
        # 如果还没有创建，则创建并显示
        container = create_tab_content(e.args)
        container.set_visibility(True)


tabs.on('update:model-value', handle_tab_change)

# 初始化第一个标签页
ui.timer(0.1, lambda: (
    logger.debug("hello"),
    # fixme: set_value 无法触发 update:model-value 事件？
    #        是 timer 的问题，还是什么问题？不对啊。这边测试发现确实不会触发？罢了。车到山前必有路，到时候再说。
    tabs.set_value('tab1'),
    tabs.update(),
    logger.debug("tabs.value: {}", tabs.value)
), once=True)

ui.button("click", on_click=lambda: tabs.set_value("tab2"))

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
