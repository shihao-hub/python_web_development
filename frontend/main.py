import random

from nicegui import ui

from menuitems.dashboard import dashboard_panel
from menuitems.account_tree import account_tree_panel
from menuitems.calculate import calculate_panel
from menuitems.solar_power import solar_power_panel
from menuitems.assessment import assessment_panel

# 菜单项
menu_items = [
    {'name': '系统概览', 'icon': 'dashboard', "fn": dashboard_panel},
    {'name': '拓扑结构', 'icon': 'account_tree', "fn": account_tree_panel},
    {'name': '潮流计算', 'icon': 'calculate', "fn": calculate_panel},
    {'name': '光伏承载力', 'icon': 'solar_power', "fn": solar_power_panel},
    {'name': '多维度评估', 'icon': 'assessment', "fn": assessment_panel},
]

# 创建主布局
with ui.row().classes('w-full h-screen'):
    # 左侧导航菜单 (1/7宽度)
    with ui.column().classes('flex-[1] bg-blue-50 h-full p-4 shadow-md'):
        # 菜单标题
        with ui.column().classes('mb-4'):
            with ui.row().classes('items-center'):
                ui.icon('bolt').classes('text-yellow-500 text-2xl mr-2')
                ui.label('柔性配电评估系统').classes('text-xl font-bold text-blue-800')
            ui.label('多维度评估与可视化平台').classes('text-xs text-blue-600 mt-1 ml-8')

        # 创建菜单项并添加点击效果
        for item in menu_items:
            def get_on_click(_item):
                return lambda: select_menu(_item)


            with ui.button(on_click=get_on_click(item)) \
                    .classes('w-full justify-start mb-2 text-blue-900') \
                    .props(f'flat icon={item["icon"]}'):
                ui.label(item['name']).classes('ml-2')

    # 右侧自定义面板 (6/7宽度)
    with ui.column().classes('flex-[6] h-full p-8'):
        # 标题区域
        selected_menu = ui.label('自定义内容面板').classes('text-2xl font-bold mb-6 text-blue-700')

        # 自定义面板容器 (留出空间供用户自定义)
        custom_panel = ui.column().classes('w-full h-11/12 bg-white rounded-lg shadow-lg p-4 border border-blue-100')
        custom_panel.style('overflow-y: auto;')

        # 初始占位内容
        with custom_panel:
            ui.label('请从左侧菜单选择功能').classes('text-gray-500 text-xl mt-10 text-center')
            ui.icon('arrow_back').classes('text-4xl text-gray-400 mx-auto mt-4')
            ui.label('此区域可用于展示电力系统数据、图表和计算结果').classes('text-center text-gray-600 mt-8')


def select_menu(item):
    selected_menu.text = f'{item["name"]} 功能面板'
    custom_panel.clear()

    if item["fn"]:
        item["fn"](custom_panel, selected_menu)
        return


select_menu(menu_items[0])

# todo: 了解 Tailwind CSS 类，比如：w-full: 宽度为父容器的 100%，h-11/12: 高度为父容器的 11/12 (约 91.67%)

# [note] 收获：ai 编程 + nicegui 可以很快做出不错的静态页面，但是微调有点复杂，可能前端就是如此？

if __name__ == '__main__':
    ui.run(title="柔性配电评估系统", host="localhost", port=12000, reload=False, show=False, favicon="🚀")
