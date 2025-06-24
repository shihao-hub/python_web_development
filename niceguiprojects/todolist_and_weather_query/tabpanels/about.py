from nicegui import ui

TITLE = "待办事项和天气查询"


def about_panel(tab):
    # 关于面板
    with ui.tab_panel(tab).classes('p-4') as about_section:
        # about_section.id = 'about-section'

        ui.label('关于本应用').classes('text-xl font-bold mb-4')

        with ui.card().classes('w-full p-6'):
            ui.markdown(f'''
                ## {TITLE}

                **功能特性:**
                - 待办事项管理（添加、完成、删除、分类）
                - 多城市天气查询
                - 响应式布局
                - 深色/浅色模式切换

                **技术栈:**
                - [NiceGUI](https://nicegui.io/) - Python Web UI 框架
                - Tailwind CSS - 样式设计
                - OpenWeatherMap API - 天气数据

                **使用方法:**
                1. 在待办事项标签页添加和管理任务
                2. 在天气标签页查看多个城市的天气
                3. 使用右上角按钮切换深色/浅色模式

                **开发信息:**
                - 开发者: zsh
                - 版本: 1.0.0
                - 开源协议: MIT
            ''').classes('prose max-w-none')

        with ui.row().classes('w-full justify-center mt-6'):
            ui.button('GitHub 仓库', icon='code',
                      on_click=lambda: ui_open("https://github.com"))
            ui.button('文档', icon='menu_book',
                      on_click=lambda: ui_open("https://nicegui.io/documentation"))
            ui.button('反馈', icon='feedback',
                      on_click=lambda: ui_open("mailto:contact@example.com"))
