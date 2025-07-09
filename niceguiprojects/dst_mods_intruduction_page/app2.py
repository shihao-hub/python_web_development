import random

from loguru import logger

from nicegui import ui
from nicegui.elements import card

import utils

TITLE = "心悦卿兮的饥荒模组合集"

# 创建自定义 CSS 样式
ui.add_css(utils.read_static_file("./index.css"))


class Dao:
    def __init__(self):
        pass

    def list(self):
        return [
            {"id": 1, "name": "智能背包系统", "description": "添加可扩展的背包系统，支持自定义分类和搜索功能",
             "tags": ["背包", "实用工具"], "downloads": 24500},
            {"id": 2, "name": "魔法科技树", "description": "扩展魔法系统，增加全新的魔法科技树和法术",
             "tags": ["魔法", "扩展内容"], "downloads": 18700},
            {"id": 3, "name": "季节优化", "description": "优化四季变化效果，添加更多季节事件和资源",
             "tags": ["环境", "优化"],
             "downloads": 32100},
            {"id": 4, "name": "怪物图鉴", "description": "添加怪物图鉴系统，记录遇到的怪物信息与弱点",
             "tags": ["怪物", "信息"],
             "downloads": 15600},
            {"id": 5, "name": "建筑大师", "description": "新增100+建筑蓝图，支持自定义建筑组合",
             "tags": ["建筑", "创造"],
             "downloads": 28900},
            {"id": 6, "name": "农业革命", "description": "彻底改革农业系统，添加新作物和耕作机制",
             "tags": ["农业", "生存"],
             "downloads": 27300},
            {"id": 7, "name": "天气控制系统", "description": "允许玩家控制天气变化，创造有利生存条件",
             "tags": ["环境", "实用工具"], "downloads": 19800},
            {"id": 8, "name": "神话生物扩展", "description": "添加20+神话生物和独特掉落物",
             "tags": ["怪物", "扩展内容"],
             "downloads": 23100},
            {"id": 9, "name": "自动化工坊", "description": "实现资源收集和加工的自动化系统", "tags": ["机械", "优化"],
             "downloads": 26500},
            {"id": 10, "name": "光影增强包", "description": "全面优化游戏光影效果，提升视觉体验",
             "tags": ["画质", "优化"],
             "downloads": 34200},
            {"id": 11, "name": "海洋探险", "description": "扩展海洋内容，添加新岛屿、海洋生物和宝藏",
             "tags": ["探索", "扩展内容"], "downloads": 21700},
            {"id": 12, "name": "生存挑战", "description": "增加生存难度，添加新的挑战机制", "tags": ["难度", "挑战"],
             "downloads": 18900},
        ]


class Service:
    def __init__(self):
        self.dao = Dao()

    def list(self):
        """模仿 django list 接口"""
        return self.dao.list()


# todo: 确定 MVC 架构并简单实践
class Controller:
    def __init__(self):
        pass


service = Service()

# 模拟模组数据
mods = service.list()

# class properties?
shared = {}


# 创建头部
def create_header():
    with ui.header().classes("header-bg w-full h-32 flex items-center justify-between px-[20%]"):
        with ui.column():
            with ui.row():
                # 左侧内容（距离左侧20%）
                with ui.row().classes("items-center gap-4"):
                    ui.icon("eco", size="lg", color="white").classes("text-3xl")
                    ui.label("心悦卿兮的饥荒模组合集").classes("text-2xl font-bold text-white")

                # 右侧开关（距离右侧20%）
                with ui.row().classes("items-center"):
                    ui.switch(on_change=lambda: logger.debug("开关切换")).props("color=white").classes("text-white")

            # 创建导航栏
            # todo: 这是全局覆盖，有问题吧
            # todo: 改为按钮，不需要用 tabs 了
            ui.add_css("""
                /* 针对选项卡标题的类名 */
                .q-tab__label {                    
                    font-size: 1.125rem !important;
                    line-height: 1.75rem !important;
                    
                    font-weight: 500 !important;
                }
            """)
            with ui.tabs() as nav_tabs:
                home_tab = ui.tab("主页").classes("hover:bg-white/10")
                moreitems_tab = ui.tab("更多物品").classes("hover:bg-white/10")
                pets_enhancement_tab = ui.tab("宠物增强").classes("hover:bg-white/10")


@ui.page("/example")
def page_example():
    ui.label("111").classes("text-lg font-medium hover:bg-white/10")


# 创建模组卡片
def create_mod_card(mod):
    with ui.card().classes("card-hover w-full h-80 relative overflow-hidden"):
        # 模组标签
        with ui.row().classes("absolute top-3 left-3"):
            for tag in mod["tags"]:
                ui.label(tag).classes("tag")

        # 模组图片
        with ui.column().classes("w-full h-32 bg-gray-200 items-center justify-center overflow-hidden"):
            # 随机生成不同的背景颜色
            colors = ["#4caf50", "#ff9800", "#2196f3", "#9c27b0", "#f44336"]
            bg_color = random.choice(colors)
            ui.element("div").style(
                f"background-color: {bg_color}; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;")
            ui.icon("extension", size="xl", color="white").classes("text-4xl")

        # 模组信息
        with ui.column().classes("p-4 flex flex-col h-48 justify-between"):
            ui.label(mod["name"]).classes("text-xl font-bold text-gray-800")
            ui.label(mod["description"]).classes("text-gray-600 text-sm mt-2 line-clamp-3")

            # 下载信息和按钮
            with ui.row().classes("w-full items-center justify-between mt-4"):
                with ui.row().classes("items-center gap-1"):
                    ui.icon("download", size="sm", color="green")
                    ui.label(f"{mod['downloads'] // 1000}k+").classes("text-gray-500 text-sm")

                ui.button("下载模组", icon="file_download").classes("download-btn px-4 py-2 rounded-full")


# 创建内容区域
def create_content():
    with ui.column().classes("w-full max-w-7xl mx-auto py-8 px-4"):
        # 标题
        # ui.label("饥荒模组合集").classes("text-4xl font-bold text-center my-12 text-gray-800")
        ui.label("饥荒模组合集").classes("mx-auto text-h2")

        # 筛选栏
        with ui.row().classes("w-full justify-center mb-8 gap-4"):
            tags = ["全部", "实用工具", "扩展内容", "优化", "画质", "生存", "创造"]
            for tag in tags:
                ui.button(tag).classes("bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-full")

        # 模组网格
        with ui.grid(columns=3).classes("w-full gap-8"):
            for mod in mods:
                create_mod_card(mod)

        # 分页
        with ui.row().classes("w-full justify-center mt-12 gap-2"):
            ui.button("1").classes("bg-green-500 text-white w-10 h-10 rounded-full")
            for i in range(2, 6):
                ui.button(str(i)).classes("bg-gray-100 hover:bg-gray-200 w-10 h-10 rounded-full")


# 创建页面
def create_page():
    # 页面结构
    create_header()
    create_content()


# 创建页面并运行
create_page()

if __name__ == '__main__':
    # todo: 注意，感觉想要使用 nicegui 模仿各自页面，还是需要去系统学习 html css，尤其 css
    ui.run(title=TITLE, favicon="🌿", host="localhost", port=15001, dark=False, reload=False, show=False)
