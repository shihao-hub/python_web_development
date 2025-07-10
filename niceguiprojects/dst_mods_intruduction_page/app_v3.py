"""
### 总结
1. 作为半吊子 nicegui 前端开发，多个版本是正常的，但是我发现，之前版本的代码编写将让你对页面结构更清晰，
   这意味着，如果你重新描述一下你的页面结构给 ai，他很有可能能够提供不错的回答！！！

"""

import functools
import json
import os
import re
import random
from abc import abstractmethod, ABC
from typing_extensions import override
from pathlib import Path
from typing import Optional, Literal, Dict, Generator, List

import markdown
import cachetools
from loguru import logger
from markdown.extensions.toc import TocExtension
from whitenoise import WhiteNoise
from dotenv import load_dotenv

from nicegui import ui, app
from nicegui.events import Handler, ValueChangeEventArguments

import settings
import utils
from settings import STATIC_DIR

load_dotenv()

TITLE = "心悦卿兮的饥荒模组合集"


class Dao(ABC):
    """数据层，最接近数据库的层级，与 Model 或者 SQL 打交道"""

    def __init__(self, model=None):
        self.model = model

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class ModInfoDao:
    def __init__(self):
        self.model = None

    def list(self) -> List[Dict]:
        """获得有序的模组信息列表"""
        # [note] mod info 数据有限，显然没必要使用 sqlite.exe，但是更多物品模组的物品介绍，我必须用，即使也不一定需要！
        return json.loads((STATIC_DIR / "data" / "modinfos.json").read_text("utf-8"))


class Service:
    """服务层，使用 Dao 层的服务，给上层提供服务"""

    def __init__(self):
        self.mod_info_dao = ModInfoDao()

    def get_mod_infos(self):
        """模仿 django list 接口，后面需要改名，目前我认为 Service 和 Dao 不是特别需要"""
        return self.mod_info_dao.list()


# todo: 确定 MVC 架构并简单实践
class Controller:
    """暂且视其为 django 的 View/Response"""

    def __init__(self):
        self.service = Service()

    def get_mod_infos(self):
        """获得各个模组的信息"""
        return self.service.get_mod_infos()

    def get_mod_item_infos(self, mod_name="更多物品"):
        """获得指定模组物品的信息"""
        raise NotImplemented

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
            yield filename, utils.read_markdown_file(filename)


class View:
    class Header(ui.header):
        def __init__(self,
                     tab_names: List[str],
                     *args,
                     logo: str = "/static/logo.jpg",
                     title: str = "心悦卿兮的模组合集",  # 只能这么长，否则我的手机上就换行了...感觉这个 title 得改成响应式...
                     **kwargs):
            super().__init__(*args, **kwargs)

            self.tabs: Dict[str, ui.tab] = {}

            with self.classes("flex flex-col p-0 gap-0"):
                with ui.row().classes("w-full items-center justify-between px-4 py-2 bg-green-500 text-white"):
                    # 左侧：图标和标题
                    with ui.row().classes("items-center gap-4"):
                        ui.image(logo).classes("w-8 h-8 rounded-full")
                        ui.label(title).classes("text-xl font-bold")

                    # 右侧：开关
                    # todo: dark_mode 需要优化，除此以外，在添加一个小眼睛图标，鼠标放上去展示访客量（手机端点击弹窗）
                    ui.switch(on_change=lambda e: ui.dark_mode(e.value))  # todo: .tooltip()
                with ui.row().classes("w-full bg-green-500 text-white"):
                    with ui.tabs().classes("w-full") as self.nav_tabs:
                        logger.info("header tab_names: {}", tab_names)
                        for tab_name in tab_names:
                            self.tabs[tab_name] = ui.tab(tab_name)

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

            with self.classes("card-hover").classes(
                    "w-full h-full shadow-lg hover:shadow-xl transition-shadow duration-300"):
                with ui.column():
                    with ui.row().classes("justify-center"):
                        with ui.grid(columns=1):
                            ui.space()
                            ui.image("/static/logo.jpg").classes("custom-mod-image")
                        with ui.column():
                            ui.label(mod["name"]).classes("text-1xl xl:text-2xl").tailwind.text_color(
                                "black").font_weight("bold")
                            ui.label(", ".join(mod["tags"])).tailwind.text_color("green-600").font_size(
                                "xl").font_weight("normal")
                    with ui.column():
                        ui.label(mod["description"]).tailwind.text_color("gray-600").font_size("base")

    class UpdateLogDialog(ui.dialog):
        """提供给更新日志模块使用的弹窗"""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            with self, ui.card():
                self.content_markdown = ui.markdown()

    class MarkdownTabPanel(ui.tab_panel):
        """更多物品模组的 ui.tab_panel"""

        def __init__(self, tab: ui.tab, doc_path: str):
            super().__init__(tab)

            with self:
                markdown_content = self.read_markdown_file(doc_path)

                # 使用响应式容器
                with ui.column().classes("w-full flex justify-center items-center p-4"):
                    # 主内容容器 - 宽度为屏幕的 3/5
                    with ui.card().classes("""
                        w-full lg:w-3/5  # 大屏幕60%宽度，小屏幕全宽
                        max-w-4xl        # 最大宽度限制
                        shadow-lg        # 阴影效果
                        rounded-lg       # 圆角
                        p-6 md:p-8       # 内边距
                        bg-white         # 背景色
                        dark:bg-gray-800 # 深色模式背景
                        transition-all   # 平滑过渡
                    """):
                        ui.markdown(markdown_content).classes("w-full prose prose-lg max-w-none dark:prose-invert")

        @staticmethod
        @cachetools.cached(cachetools.TTLCache(maxsize=10, ttl=2))
        def read_markdown_file(relative_path: str) -> str:
            filepath = STATIC_DIR / "markdown" / relative_path
            if not filepath.exists():
                return """文档不存在"""
            return filepath.read_text("utf-8")

    def __init__(self):
        self.controller = Controller()

        ui.add_css(utils.read_static_file("./index.css"))

        # 定义，避免重复创建
        self.dark = ui.dark_mode()
        self.update_log_dialog = self.UpdateLogDialog()

        # 页面结构
        self._create_header()
        self._create_content()
        self._create_footer()

        # 注册 timer
        self.register_timer()

    def register_timer(self):
        # todo: 似乎可以被取代？tab active？
        ui.timer(0.1, lambda: self.nav_tabs.set_value(self.tabs["主页"]), once=True)

        if settings.DEBUG:
            ui.timer(0.5, lambda: self.nav_tabs.set_value(self.tabs["更多物品"]), once=True)

        # todo: 练习一下，加载完弹出一个公告 dialog

        # todo: 需要记住客户端的信息，比如现在在哪个 tab，加载完成后，定位到哪里！至于客户端信息，建议只需要单纯 k:v

    def _create_header(self):
        self.header = self.Header([
            "主页",
            *[e["name"] for e in self.controller.get_mod_infos()],
            "更新日志",
            "错误反馈",
        ])

        # 兼容
        self.nav_tabs = self.header.nav_tabs
        self.tabs = self.header.tabs

    def _create_home_panel(self):
        with ui.tab_panel(self.tabs["主页"]).classes("w-full justify-center items-center"):
            ui.label("饥荒模组合集").classes("md:mx-auto text-h4")

            with ui.grid().classes("w-full gap-y-8 grid-cols-1 sm:grid-cols-2 xl:grid-cols-3"):
                for mod in self.controller.get_mod_infos():
                    card = self.ModInfoCard(mod).classes("justify-self-center")
                    card.on("click", functools.partial(
                        lambda mod, e: self.nav_tabs.set_value(self.tabs[mod["name"]]), mod))

    def _create_update_log_panel(self):
        # todo: css 的 inherit、initial、unset、revert：https://cloud.tencent.com/developer/article/2312895
        # .style("width: 100%;") 让 tab_panel 与 tab_panels 宽度对齐，但是这似乎意味着 tab_panels 也需要修改，我不建议
        with ui.tab_panel(self.tabs["更新日志"]).classes("w-full"):
            with ui.column().classes("w-full gap-y-4"):
                # todo: tab_panel flex，导致其内部组件的长宽会被根据其内容限定？真的吗？
                #       不对，w 似乎被什么预先限制了！w-full 好像是看他的父容器的？但是不应该呀！
                #       唉，哪怕只是样式的轻微改动优化，作为半吊子前端，根本不行！请系统学习 html css，js 倒不需要！
                #       测试发现：
                #       .nicegui-tab-panel 的 display: flex; 取消掉就行，但是显然有点小问题，得找到一种方式，
                #       轻微进行覆盖比较好，比如添加 classes, style 尝试覆盖顶层（嗯？行内 style 是不是强一点）
                #       .style("display: revert !important;")
                for filename, content in self.controller.get_update_log_mardown_files():
                    # todo: 优化 card 及其内部 markdown
                    with ui.card().classes("w-full h-80 overflow-auto"):
                        with ui.row():  # todo: 让其中的元素居于中轴
                            # https://quasar.dev/vue-components/spinners#qspinner-api
                            # fixme: hidden sm:block 根本不生效啊！
                            ui.spinner("ball", size="lg", color="green").classes("hidden xl:block")

                            with ui.column().classes("pt-2"):
                                # todo: 点击弹出弹窗展示
                                title = ui.label(f"{filename[:-3]}")
                                title.tooltip("点击预览")
                                title.classes("cursor-pointer hover:text-blue-500")  # hover:underline
                                title.tailwind.text_color("black").font_weight("bold").font_size("2xl")
                                # click | dblclick
                                title.on("click", functools.partial(lambda content: (
                                    logger.debug("[update-log] title click"),
                                    self.update_log_dialog.content_markdown.set_content(content),
                                    self.update_log_dialog.open()
                                ), content))

                            # todo: 如果添加这个，需要将其放在最右侧才行
                            # ui.button("Download", on_click=lambda: ui.download(f"/static/markdown/{filename}"))

                        ui.separator()
                        # todo: 推荐美化一下？还是说 markdown 也能支持图片嵌入渲染的能力？
                        # 此处的超长 classes 是 ai 生成的，默认的 h1 h2 h3 太大了
                        ui.markdown(content).classes("""
                                    prose 
                                    prose-h1:text-4xl prose-h1:font-bold prose-h1:text-blue-700 prose-h1:mt-8 prose-h1:mb-4
                                    prose-h2:text-3xl prose-h2:font-semibold prose-h2:text-blue-600 prose-h2:mt-7 prose-h2:mb-3
                                    prose-h3:text-2xl prose-h3:font-medium prose-h3:text-blue-500 prose-h3:mt-6 prose-h3:mb-2
                                    prose-h4:text-xl prose-h4:font-medium prose-h4:text-indigo-500 prose-h4:mt-5 prose-h4:mb-2
                                    prose-h5:text-lg prose-h5:font-normal prose-h5:text-indigo-400 prose-h5:mt-4 prose-h5:mb-1
                                    prose-h6:text-base prose-h6:font-normal prose-h6:text-indigo-300 prose-h6:mt-3 prose-h6:mb-1
                                    prose-p:my-3
                                    prose-ul:my-2
                                    prose-ol:my-2
                                    prose-blockquote:border-l-4 prose-blockquote:border-blue-300 prose-blockquote:pl-4 prose-blockquote:py-1 prose-blockquote:bg-blue-50
                                    prose-code:bg-gray-100 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded
                                    prose-pre:bg-gray-800 prose-pre:text-gray-100
                                    max-w-none
                                """)

    def _create_content(self):
        with ui.tab_panels(self.nav_tabs).classes("w-full"):
            self._create_home_panel()
            # todo: 左侧目录栏是有必要实现的，右侧可以选择不需要，要不添加一个单纯的活动式菜单栏？点击可以缩小成一个按钮。
            self.MarkdownTabPanel(self.tabs["更多物品"], "./更多物品.md")
            self.MarkdownTabPanel(self.tabs["宠物增强"], "./宠物增强.md")
            self.MarkdownTabPanel(self.tabs["复活按钮和传送按钮"], "./复活按钮和传送按钮.md")
            self.MarkdownTabPanel(self.tabs["便携大箱子"], "./便携大箱子.md")
            self._create_update_log_panel()

    def _create_footer(self):
        # todo: 暂且计划是加一个不算明显的 footer，用于记录一些信息，比如点击量，访问量等
        pass


@ui.page("/")
def page_index():
    # todo: 能不能写出一个通用的移动端和桌面端的页面？不要搞得移动端直接面目全非。
    #       比如就目前的实现，header 移动端直接面目全非，tabs 还消失了，绷不住。
    # fixme: 速速考虑一下！
    View()


@ui.page("/moreitems")
def page_moreitems():
    pass


@ui.page("/example")
def page_example():
    from nicegui import ui

    grid = ui.aggrid({
        'defaultColDef': {'flex': 1},
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
            {'headerName': 'Parent', 'field': 'parent', 'hide': True},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18, 'parent': 'David'},
            {'name': 'Bob', 'age': 21, 'parent': 'Eve'},
            {'name': 'Carol', 'age': 42, 'parent': 'Frank'},
        ],
        'rowSelection': 'multiple',
    }).classes('max-h-40')

    def create_two_line_header():
        # 创建顶部固定容器
        with ui.header().classes('flex flex-col p-0 gap-0'):
            # 第一行
            with ui.row().classes('items-center justify-between w-full px-4 py-2 bg-blue-800 text-white'):
                # 左侧：图标和标题
                with ui.row().classes('items-center gap-4'):
                    ui.image('https://nicegui.io/logo_square.png').classes('w-8 h-8')
                    ui.label('应用标题').classes('text-xl font-bold')

                # 右侧：开关
                ui.switch('深色模式')

            # 第二行：标签页
            with ui.row().classes('w-full bg-blue-800 text-white'):
                tabs = ui.tabs().classes('w-full')
                with tabs:
                    for tab_name in [
                        '首页',
                        '产品',
                        '服务',
                        '关于我们',
                        '联系我们'
                    ]:
                        ui.tab(tab_name)

    # 创建两行标题
    create_two_line_header()

    # 页面内容区域
    with ui.column().classes('w-full p-8 gap-4'):
        ui.label('页面内容区域').classes('text-2xl')
        ui.button('示例按钮')
        ui.slider(min=0, max=100, value=50)


# 使本地目录在指定的端点可用，这对于向前端提供本地数据（如图像）非常有用
# todo: 是否需要处理缓存问题，这每次传送这么多静态资源的话？
# app.mount('/static', WhiteNoise(directory=str(STATIC_DIR), max_age=600))
app.add_static_files("/static", "./static")

if __name__ == '__main__':
    # todo: 注意，感觉想要使用 nicegui 模仿各自页面，还是需要去系统学习 html css，尤其 css
    ui.run(title=TITLE, favicon="🌿", host="localhost", port=15001, dark=False, reload=False, show=False,
           on_air=os.getenv("NICEGUI_TOKEN"))
