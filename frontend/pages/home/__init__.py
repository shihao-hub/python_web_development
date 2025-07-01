from nicegui import ui

from .panels.dashboard_panel import dashboard_panel
from .panels.account_tree_panel import account_tree_panel
from .panels.calculate_panel import calculate_panel
from .panels.solar_power_panel import solar_power_panel
from .panels.assessment_panel import assessment_panel

# 菜单项
menu_items = [
    {'name': '系统概览', 'icon': 'dashboard', "fn": dashboard_panel},
    {'name': '拓扑结构', 'icon': 'account_tree', "fn": account_tree_panel},
    {'name': '潮流计算', 'icon': 'calculate', "fn": calculate_panel},
    {'name': '光伏承载力', 'icon': 'solar_power', "fn": solar_power_panel},
    {'name': '多维度评估', 'icon': 'assessment', "fn": assessment_panel},
]


# todo: 确定一下 __init__.py 中推荐执行代码吗？
# todo: async def main 和 def main 都可以被 ui.page 修饰？
# todo: 好好深入 nicegui
# todo: 多阅读框架源代码，多学习吸收优秀的代码
# todo: 确定 ui.page 和不设置的区别 | 全局变量不同页面是否独立 | 页面间数据传递 | ui.page 做了什么，请深入 vue ...
@ui.page("/")
def main():
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
            custom_panel = ui.column().classes(
                'w-full h-11/12 bg-white rounded-lg shadow-lg p-4 border border-blue-100')
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

    # todo: 弄明白 python async 不同调用方式的区别，为什么 ide 无法智能提示？

    # todo: 页面加载完的一瞬间，立刻发出一个权限探测请求，用于检测用户权限，并返回结果
    # [answer] 这个有待深入，目前不知道该如何实现，但是显然刷新的时候肯定会调用后端请求来获取数据，
    #          那么我认为后端不应该重定向，而是返回指定响应，由前端重定向！

    # todo: 了解 Tailwind CSS 类，比如：w-full: 宽度为父容器的 100%，h-11/12: 高度为父容器的 11/12 (约 91.67%)

    # [note] 收获：ai 编程 + nicegui 可以很快做出不错的静态页面，但是微调有点复杂，可能前端就是如此？

    # 测试发现，select_menu 为什么会一直被执行？nicegui 不知道原理的话实在有些痛苦
    select_menu(menu_items[0])
