"""
### 需求背景
在《Don't Starve Together》游戏中，玩家可能会遇到各种模组，但可能不知道如何使用它们。
因此，我们需要一个介绍页面，向玩家展示如何使用这些模组。

### 需求详情
- 介绍页主要是多个选项卡，每个选项卡代表一个模组
- 点击选项卡后跳转到对应的模组介绍页，模组介绍页需要提供如下功能：
  - 需要提供搜索功能（这个需要设定一下，目前主要理解为筛选功能，表格的筛选功能）
  - 需要提供模组的一些介绍
  - 需要使用表格展示模组的物品信息（推荐使用 json 文件作为配置文件，然后 update_or_create mongodb 实现）
    - 物品名称
    - 物品贴图
    - 物品描述

### 编程要求
1. ai 生成的所有涉及 style，classes 的代码一律不能直接复制，必须弄明白各个内容的作用（理想情况，总之必须有意识地学习一下）
2. 作为前端初学者，前端的骨架和皮肤应当学习参考各种现成的页面，类似语文作文，多读文章才能下笔如有神。

### 设计参考
1. https://dont-starve-mod.github.io/zh/home/

"""
import functools
from typing import List

from loguru import logger

from nicegui import ui

import settings
import utils


class _component_center_upvalues:  # noqa: Redeclared '{0}' defined above without usage
    """临时使用，充当 singleton dict [tip] 显然可以隐藏细节吧，不管如何实现的？"""
    components: set = set()

    @classmethod
    def print_components(cls):
        """临时使用，打印 components"""
        print(cls.components)


def decorator_component_center(func):
    """临时使用，汇总通过函数注册的组件个数"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        _component_center_upvalues.components.add(res)
        return res

    return wrapper


@ui.page("/upgrading")
def page_upgrading():
    """升级/维护页面"""
    # 页面样式
    # todo: 确定一下 nicegui 推荐如此自定义样式吗？首先有原有样式冲突的可能，其次开发过于不便等
    # todo: 速速了解 css 基础语法（早忘光了）
    ui.add_css(utils.read_static_file("./upgrading.css"))

    MAINTENANCE_INFO = {  # noqa: Variable in function should be lowercase
        "title": "系统维护中",
        "subtitle": "我们正在进行系统升级，以提供更好的服务体验",
        "contact": "QQ 群号：592159151"
    }

    # 创建维护卡片
    with ui.element('div').classes('maintenance-card mx-auto'):
        # 维护图标
        ui.icon('construction').classes('construction-icon')

        # 标题
        ui.label(MAINTENANCE_INFO['title']).classes('title')

        # 副标题
        ui.label(MAINTENANCE_INFO['subtitle']).classes('subtitle')

        # 联系信息
        with ui.element('div').classes('contact'):
            ui.icon('support_agent')
            ui.label(MAINTENANCE_INFO['contact'])


# todo: 为什么加上装饰器后，该方法被使用的时候，ide 不提示：Parameter '{0}' unfilled
# @decorator_component_center
def create_mod_info_card(icon: str, title: str, tags: List[str], description: str) -> ui.card:
    with ui.card().classes("w-96 h-48") as card:
        with ui.row():
            ui.icon(icon).classes('q-mr-md')
            with ui.column():
                ui.label(title).classes('text-h6 q-mt-sm')
                ui.label(", ".join(tags)).classes('text-subtitle2 q-mt-sm')
        ui.label(description).classes('text-body1 q-mt-sm')
    return card


@ui.page("/")
def page_index():
    # todo: 拦截全局请求（除了 /upgrading 自己），一律重定向到其中。或者单页面应用开发？
    if settings.UPGRADING:
        ui.navigate.to("/upgrading")

    with ui.header().style("background-color: #4cae4f"):
        icon = ui.icon("home")
        title = ui.label("心悦卿兮的饥荒模组合集")
        ui.space()  # todo: 确定是否需要这个，实际应该也可以通过 css 实现
        switch = ui.switch()

    # with ui.footer().style("border-color: #000; border-width: 2px; border-style: solid;"):
    #     pass

    # todo: ui.tabs() 紧挨着 headers，二者背景需要保证一致

    # todo: tabs 无法懒加载吧？所以后面还是需要改动（tabs 应该是 <a> List，点击跳转，各个页面的 header 和 footer 相同）
    with ui.element("div").classes("w-full"):
        with ui.tabs().style("background-color: #4cae4f") as nav_tabs:
            # todo: 设置为从 json 配置文件中获取（mongodb）
            home_tab = ui.tab("主页")
            moreitems_tab = ui.tab("更多物品")

    # tab_panels 似乎是跟随 tabs 的？
    with ui.tab_panels(nav_tabs, value=home_tab).classes("mx-auto"):
        with ui.tab_panel(home_tab):
            with ui.column():
                ui.label("饥荒模组合集").classes("mx-auto text-h2")
                with ui.grid(columns=3):
                    # todo: 封装成函数/类（注意函数也是类的封装思想罢了）
                    # todo: 实现鼠标放上去的动态浮动效果
                    create_mod_info_card("home", "更多物品", ["联机", "物品"], "新增 80+ 种物品")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")
                    create_mod_info_card("home", "宠物增强", ["联机", "宠物"], "修改原版宠物")

        with ui.tab_panel(moreitems_tab) as moreitems_panel:
            # todo: 查看有哪些事件
            moreitems_panel.on("click", lambda *args: logger.info(args))
            ui.label("更多物品内容")


if __name__ == '__main__':
    # todo: 根据文件名计算出来一个端口号（要求每次计算结果都应该一样）
    # todo: 探索 dark=True 做了什么，至少一点，改了 dark 组件的边界有的能直接看到了，哈哈，也可以助力开发
    ui.run(host="localhost", port=15000, reload=False, show=False, favicon="🚀")
