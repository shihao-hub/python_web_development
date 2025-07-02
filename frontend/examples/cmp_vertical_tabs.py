from loguru import logger

from nicegui import ui

with ui.splitter(value=30).classes('w-full h-56') as splitter:
    with splitter.before:
        with ui.tabs().props('vertical').classes('w-full') as tabs:
            mail = ui.tab('Mails', icon='mail')
            alarm = ui.tab('Alarms', icon='alarm')
            movie = ui.tab('Movies', icon='movie')
    with splitter.after:
        with ui.tab_panels(tabs, value=mail) \
                .props('vertical').classes('w-full h-full'):
            with ui.tab_panel(mail):
                ui.label('Mails').classes('text-h4')
                ui.label('Content of mails')
            with ui.tab_panel(alarm):
                ui.label('Alarms').classes('text-h4')
                ui.label('Content of alarms')
            with ui.tab_panel(movie):
                ui.label('Movies').classes('text-h4')
                ui.label('Content of movies')

# todo: tabs 数据一直在没问题，主要不要过度啊，比如无时无刻调用接口，肯定是有问题的
# todo: 可以在切换的时候在调用，一个建议，每个图标建议设置一个 loading 遮盖。
# todo: 默认情况怎么办？

tabs.on('update:model-value', lambda e: logger.debug("{}", e.args))

ui.timer(0, lambda: (
    logger.debug("{}", tabs.value),
    tabs.set_value(mail),
    logger.debug("2: {}", tabs.value),
    tabs.update()
), once=True)

# ui.run()
ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
