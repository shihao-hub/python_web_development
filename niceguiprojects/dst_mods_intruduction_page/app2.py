import functools
import os
import re
import random
from pathlib import Path
from typing import Optional, Literal, Dict, Generator

import cachetools
from loguru import logger

from nicegui import ui, app

import settings
import utils
from settings import STATIC_DIR

TITLE = "心悦卿兮的饥荒模组合集"


class Dao:
    """数据层，最接近数据库的层级，与 Model 或者 SQL 打交道"""

    def __init__(self):
        pass

    def list(self):
        return [
            {"id": 1, "name": "更多物品", "description": "新增 80+ 种物品",
             "tags": ["联机", "物品", "辅助"]},
            {"id": 2, "name": "宠物增强", "description": "修改原版宠物",
             "tags": ["联机", "宠物"]},

            {"id": 3, "name": "宠物增强", "description": "修改原版宠物",
             "tags": ["联机", "宠物"]},
            {"id": 4, "name": "宠物增强", "description": "修改原版宠物",
             "tags": ["联机", "宠物"]},
            {"id": 5, "name": "宠物增强", "description": "修改原版宠物",
             "tags": ["联机", "宠物"]},
            {"id": 6, "name": "宠物增强", "description": "修改原版宠物",
             "tags": ["联机", "宠物"]},
            {"id": 7, "name": "宠物增强", "description": "修改原版宠物",
             "tags": ["联机", "宠物"]},
        ]


class Service:
    """服务层，使用 Dao 层的服务，给上层提供服务"""

    def __init__(self):
        self.dao = Dao()

    def list(self):
        """模仿 django list 接口"""
        return self.dao.list()


# todo: 确定 MVC 架构并简单实践
class Controller:
    """暂且视其为 django 的 View/Response"""

    def __init__(self):
        self.service = Service()

    def get_mod_items_info(self, mod_name="更多物品"):
        return self.service.list()

    def get_update_log_mardown_files(self):  # todo:  -> Generator[str] 如何使用？
        """读取指定文件名格式的 markdown 文件，并排序返回内容列表的生成器"""
        markdown_dir = STATIC_DIR / "markdown"
        pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})-更新日志\.md$')
        filenames = []
        for filename in os.listdir(markdown_dir):
            full_path = markdown_dir / filename
            if full_path.is_dir():
                continue
            if not full_path.suffix == ".md":
                continue
            if not pattern.match(filename):
                continue
            filenames.append(filename)
        filenames = sorted(filenames, reverse=True)
        logger.debug("markdown files: {}", filenames)
        # 由于 filename 是 YYYY-MM-DD-更新日志.md 格式，所以将其从大到小排列即可
        for filename in filenames:
            yield f"### {filename[:-3]}\n" + utils.read_markdown_file(filename)


class View:
    class ModInfoCard(ui.card):
        """暂且使用的隔离方式是将 components 作为 View 的内部类"""

        # todo: 注意，for 循环生成的组件，都应该被抽成类？好像也还好，只有 for + 闭包 才有问题。
        def __init__(self, mod: Dict, *args, **kwargs) -> None:
            """
            参数：
                mod:Dict 模组信息 todo: 此处可以用 dataclass
            """
            super().__init__(*args, **kwargs)

            # 类实例化等价于调用方法。所以可以理解为，类是高级一点的函数！

            # todo: 暂且如此，这个样式 card 的样式是需要修改的！
            with self.classes("card-hover").classes("w-96 h-52 relative overflow-hidden"):
                # 模组标签
                with ui.row().classes("absolute top-3 left-3"):  # todo: 这个 top-3 left-3，感觉 css 就是需要知道原理...
                    for tag in mod["tags"]:
                        ui.label(tag).classes("tag")

                # 模组图片
                with ui.column().classes("w-full h-32 bg-gray-200 items-center justify-center overflow-hidden"):
                    # 随机生成不同的背景颜色
                    colors = ["#4caf50", "#ff9800", "#2196f3", "#9c27b0", "#f44336"]
                    bg_color = random.choice(colors)
                    ui.element("div").classes("custom-mod-info-image").style(f"background-color: {bg_color};")
                    # todo: 这个 extension 很逗，而且很特别
                    # ui.icon("extension", size="xl", color="white").classes("text-4xl")

                # 模组信息
                with ui.column().classes("p-4 flex flex-col h-48 justify-between"):
                    ui.label(mod["name"]).classes("text-xl font-bold text-gray-800")
                    ui.label(mod["description"]).classes("text-gray-600 text-sm mt-2 line-clamp-3")

    def __init__(self):
        self.controller = Controller()

        ui.add_css(utils.read_static_file("./index.css"))

        # 单例定义，避免重复创建
        self.dark = ui.dark_mode()

        # 页面结构
        self._create_header()
        self._create_content()
        self._create_footer()

        # timer
        ui.timer(0.1, lambda: self.nav_tabs.set_value(self.tabs["主页"]), once=True)
        # test
        # ui.timer(0.5, lambda: self.nav_tabs.set_value(self.tabs["更新日志"]), once=True)

    def on_dark_switch_change(self, e):
        if e.value:
            self.dark.enable()
        else:
            self.dark.disable()

    def _create_header(self):
        # [tip] .tailwind 虽然有提示，但是 with xxx 不能用啊，本来还想着能区别一下，熟悉这个 css 是 tailwind 呢...
        # todo: 能否不用自定义 css 呢？比如 header-bg 自定义就导致没有兼容 ui.dark_mode
        with ui.header().classes("header-bg").classes("w-full h-28"):
            with ui.column().classes("w-full gap-y-0 mr-12 ml-12"):
                with ui.row().classes("w-full justify-between items-center"):
                    with ui.row():
                        # 左侧内容（距离左侧20%）
                        ui.image("/static/logo.jpg").classes("small-rounded-image")
                        ui.label("心悦卿兮的饥荒模组合集").classes("text-2xl font-bold text-white")

                    with ui.row():
                        # 右侧开关（距离右侧20%）
                        ui.switch(on_change=self.on_dark_switch_change).props("color=white").classes("text-white")

                # 创建导航栏
                self.tabs: Dict[str, ui.tab] = {}
                with ui.tabs() as self.nav_tabs:
                    self.tabs["主页"] = ui.tab("主页").classes("hover:bg-white/10")

                    # todo: mod info table 应该要添加排序字段，或者可以调整行序，否则前端无法按序生成，且保证每次一样
                    self.tabs["更多物品"] = ui.tab("更多物品").classes("hover:bg-white/10")
                    self.tabs["宠物增强"] = ui.tab("宠物增强").classes("hover:bg-white/10")

                    self.tabs["更新日志"] = ui.tab("更新日志").classes("hover:bg-white/10")

    def _create_content(self):
        # with ui.column().classes("w-full max-w-5xl mx-auto py-8 px-4").style("padding-top: 0rem;"):
        with ui.tab_panels(self.nav_tabs).classes("ml-8").style("width: 95%;"):  # todo: 我有点好奇，为什么 tab_panels 默认是向左偏移的？
            # todo: 解决那边，这边问题又来了，tabs tab 不是好选择啊，感觉他们得都一样
            with ui.tab_panel(self.tabs["主页"]).classes("ml-8"):
                def create_home_panel():
                    # 标题
                    # ui.label("饥荒模组合集").classes("text-4xl font-bold text-center my-12 text-gray-800")
                    ui.label("饥荒模组合集").classes("mx-auto text-h4")

                    # 【暂不需要】筛选栏
                    # with ui.row().classes("w-full justify-center mb-8 gap-4"):
                    #     tags = ["全部", "实用工具", "扩展内容", "优化", "画质", "生存", "创造"]
                    #     for tag in tags:
                    #         ui.button(tag).classes("text-gray-700 px-4 py-2 "
                    #                                "bg-gray-100 hover:bg-gray-20 "
                    #                                "rounded-full ")

                    # 模组网格
                    # todo: 能否做到某一行动态？比如只有第一行和最后一行，最后一行一个的时候居中，两个的时候平衡一下
                    with ui.grid(columns=3).classes("w-full gap-8"):
                        # [note] 此处在初始化的时候就获取数据，此处显然可以理解为 django 的 templates 机制
                        for mod in self.controller.get_mod_items_info():
                            card = self.ModInfoCard(mod)
                            # todo: 确保此处的 name 和 ui.tab 绑定
                            card.on("click", functools.partial(
                                lambda mod, e: self.nav_tabs.set_value(self.tabs[mod["name"]]), mod))

                    # 【暂不需要】分页 - 点击按钮调用接口然后刷新相应组件
                    # with ui.row().classes("w-full justify-center mt-12 gap-2"):
                    #     ui.button("1").classes("bg-green-500 text-white w-10 h-10 rounded-full")
                    #     for i in range(2, 6):
                    #         ui.button(str(i)).classes("bg-gray-100 hover:bg-gray-200 w-10 h-10 rounded-full")

                create_home_panel()
            # todo: css 的 inherit、initial、unset、revert：https://cloud.tencent.com/developer/article/2312895
            with ui.tab_panel(self.tabs["更新日志"]).classes("w-full").style("width: 100%;"):
                def create_update_log_panel():
                    with ui.column().classes("w-full gap-y-4"):
                        # todo: tab_panel flex，导致其内部组件的长宽会被根据其内容限定？真的吗？
                        #       不对，w 似乎被什么预先限制了！w-full 好像是看他的父容器的？但是不应该呀！
                        #       唉，哪怕只是样式的轻微改动优化，作为半吊子前端，根本不行！请系统学习 html css，js 倒不需要！
                        #       测试发现：
                        #       .nicegui-tab-panel 的 display: flex; 取消掉就行，但是显然有点小问题，得找到一种方式，
                        #       轻微进行覆盖比较好，比如添加 classes, style 尝试覆盖顶层（嗯？行内 style 是不是强一点）
                        #       .style("display: revert !important;")
                        for content in self.controller.get_update_log_mardown_files():
                            with ui.card().classes("w-full h-64 overflow-auto"):
                                ui.markdown(content)

                create_update_log_panel()

            # todo: 尝试高级表格、第三方库等（分页等...）
            with ui.tab_panel(self.tabs["更多物品"]):
                pass

            with ui.tab_panel(self.tabs["宠物增强"]):
                pass

    def _create_footer(self):
        pass


@ui.page("/")
def page_index():
    # todo: 能不能写出一个通用的移动端和桌面端的页面？不要搞得移动端直接面目全非。
    #       比如就目前的实现，header 移动端直接面目全非，tabs 还消失了，绷不住。
    # fixme: 速速考虑一下！
    View()


# 使本地目录在指定的端点可用，这对于向前端提供本地数据（如图像）非常有用
# todo: 是否需要处理缓存问题，这每次传送这么多静态资源的话？
app.add_static_files("/static", "./static")

if __name__ == '__main__':
    # todo: 注意，感觉想要使用 nicegui 模仿各自页面，还是需要去系统学习 html css，尤其 css
    ui.run(title=TITLE, favicon="🌿", host="localhost", port=15001, dark=False, reload=False, show=False)
