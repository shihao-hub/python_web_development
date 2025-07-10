import functools
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

from nicegui import ui, app

import settings
import utils
from settings import STATIC_DIR

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
        return [
            {"id": 1, "name": "更多物品", "description": "新增 80+ 种物品",
             "tags": ["联机", "物品", "辅助"]},
            {"id": 2, "name": "宠物增强", "description": "修改原版宠物",
             "tags": ["联机", "宠物"]},
            {"id": 3, "name": "复活按钮和传送按钮", "description": "暂无",
             "tags": ["联机"]},
            {"id": 4, "name": "便携大箱子", "description": "暂无",
             "tags": ["联机"]},
        ]


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

            with self.classes("card-hover").classes("w-96 h-52"):
                with ui.column():
                    with ui.row().classes("justify-center"):
                        with ui.grid(columns=1):
                            ui.space()
                            ui.image("/static/logo.jpg").classes("custom-mod-image")
                        with ui.column():
                            ui.label(mod["name"]).tailwind.text_color("black").font_size("2xl").font_weight("bold")
                            ui.label(", ".join(mod["tags"])).tailwind.text_color("green-600").font_size(
                                "xl").font_weight("normal")
                    with ui.column():
                        ui.label(mod["description"]).tailwind.text_color("gray-600").font_size("base")

        def version_1_0(self, mod: Dict):
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

    class UpdateLogDialog(ui.dialog):
        """提供给更新日志模块使用的弹窗"""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            with self, ui.card():
                self.content_markdown = ui.markdown()

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

        # test
        ui.timer(0.5, lambda: self.nav_tabs.set_value(self.tabs["更多物品"]), once=True)

        # todo: 练习一下，加载完弹出一个公告 dialog

        # todo: 需要记住客户端的信息，比如现在在哪个 tab，加载完成后，定位到哪里！至于客户端信息，建议只需要单纯 k:v

    def on_dark_switch_change(self, e):
        if e.value:
            self.dark.enable()
        else:
            self.dark.disable()

    def _create_header(self):
        # [tip] .tailwind 虽然有提示，但是 with xxx 不能用啊，本来还想着能区别一下，熟悉这个 css 是 tailwind 呢...
        # todo: 能否不用自定义 css 呢？比如 header-bg 自定义就导致没有兼容 ui.dark_mode
        # [note] 注意，请以追求放大不错位为目标，所以尽量减少绝对值等使用方式
        with ui.header().classes("header-bg").classes("w-full h-28"):
            # todo: 说实话，想要动态比例，显然应该涉及 css 计算，拿到父容器 width，然后实时计算得到子的...
            # [note] .style("margin-left: auto;margin-right: auto;max-width: 80rem;") 可以实现居中且放大不出问题...
            with ui.column().classes("temporary-custom-centered").classes("w-full gap-y-0"):
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
                # todo: 需要整个支持水平拖动，为了兼容移动端等
                with ui.tabs() as self.nav_tabs:
                    self.tabs["主页"] = ui.tab("主页").classes("hover:bg-white/10")

                    for modinfo in self.controller.get_mod_infos():
                        self.tabs[modinfo["name"]] = ui.tab(modinfo["name"]).classes("hover:bg-white/10")

                    self.tabs["更新日志"] = ui.tab("更新日志").classes("hover:bg-white/10")
                    # todo: 主要提供一些作者的联系方式，不建议添加评论区，因为没有审核怎么办？
                    self.tabs["错误反馈"] = ui.tab("错误反馈").classes("hover:bg-white/10")

    def _create_content(self):
        # with ui.column().classes("w-full max-w-5xl mx-auto py-8 px-4").style("padding-top: 0rem;"):
        # .style("width: 95%;") 可以让 tab_panels 与其父模板宽度对齐，但是 tab_panels 涉及所有选项卡了怎么办？
        with ui.tab_panels(self.nav_tabs).classes("w-full"):
            # todo: 需要此处的内容左右偏移，这个之后解决吧，找个通用方案就行
            with ui.tab_panel(self.tabs["主页"]).classes("temporary-custom-centered").classes(
                    "w-full justify-center items-center"):
                def create_home_panel():
                    # 标题
                    # ui.label("饥荒模组合集").classes("text-4xl font-bold text-center my-12 text-gray-800")
                    ui.label("饥荒模组合集").classes("md:mx-auto text-h4")

                    # 【暂不需要】筛选栏
                    # with ui.row().classes("w-full justify-center mb-8 gap-4"):
                    #     tags = ["全部", "实用工具", "扩展内容", "优化", "画质", "生存", "创造"]
                    #     for tag in tags:
                    #         ui.button(tag).classes("text-gray-700 px-4 py-2 "
                    #                                "bg-gray-100 hover:bg-gray-20 "
                    #                                "rounded-full ")

                    # 模组网格
                    # todo: 能否做到某一行动态？比如只有第一行和最后一行，最后一行一个的时候居中，两个的时候平衡一下
                    with ui.grid(columns=3).classes("w-full gap-y-8"):
                        # [note] 此处在初始化的时候就获取数据，此处显然可以理解为 django 的 templates 机制
                        for mod in self.controller.get_mod_infos():
                            # todo: 需要兼容移动端！
                            card = self.ModInfoCard(mod).classes("justify-self-center")
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
            # .style("width: 100%;") 让 tab_panel 与 tab_panels 宽度对齐，但是这似乎意味着 tab_panels 也需要修改，我不建议
            with ui.tab_panel(self.tabs["更新日志"]).classes("w-full"):
                def create_update_log_panel():
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
                                    ui.spinner("ball", size="lg", color="green")

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

                create_update_log_panel()

            # todo: 尝试高级表格、第三方库等（分页等...）
            # todo: 能否集成专门的博客面板？（左侧目录，中间内容，右侧其他）
            with ui.tab_panel(self.tabs["更多物品"]):
                def create_moreitems_panel():
                    @cachetools.cached(cachetools.TTLCache(maxsize=10, ttl=2))
                    def read_moreitems_file() -> str:
                        filepath = STATIC_DIR / "markdown" / "moreitems.md"
                        return filepath.read_text("utf-8")

                    markdown_content = read_moreitems_file()

                    def extract_titles(md_text: str) -> list:
                        """提取标题层级结构"""
                        res = []
                        for line in md_text.split('\n'):
                            line = line.strip()
                            if line.startswith('#'):
                                logger.debug("line: {}", line)
                                level = line.count('#', 0, 6)  # 获取标题级别 (1-6)
                                title_text = line.lstrip('#').strip()
                                res.append((level, title_text))
                        logger.debug("extract_titles: {}", res)
                        return res

                    def generate_toc(md_text: str) -> str:
                        """生成带锚点的目录 HTML"""
                        html = markdown.markdown(md_text, extensions=[TocExtension(toc_depth="2-3", anchorlink=True)])
                        logger.debug("html: {}", html)
                        toc_match = re.search(r'<div class="toc">(.*?)</div>', html, re.DOTALL)
                        res = toc_match.group(1) if toc_match else ""
                        logger.debug("generate_toc: {}", res)
                        return res

                    # fixme: 处理 Markdown 内容，目前处理的有问题
                    titles = extract_titles(markdown_content)
                    toc_html = generate_toc(markdown_content)

                    # todo: title_css 和 defualt_title_css 似乎可以用一个类
                    title_css = {
                        0: "text-lg font-bold",

                        1: "text-lg font-bold",
                        2: "text-md pl-4",
                        3: "text-sm pl-8",

                        4: "text-sm pl-8",
                        5: "text-sm pl-8",
                    }
                    defualt_title_css = "text-sm pl-8"

                    # todo: 让左侧和右侧同 header 一样，y 轴滚动的时候依旧跟随（top-*？）
                    # fixme: row 中的三个元素 flex 的情况下，分辨率变小，右侧很容易到下面去了... 不想这样！
                    with ui.row().classes("temporary-custom-centered").classes('w-full h-full gap-12'):
                        # todo: 此处需要变成转移动端后，自动收缩并在左上角显示一个按钮...
                        #       实在不行，就隐藏左侧和右侧的内容吧！
                        # 左侧标题导航
                        with ui.column().classes("w-1/6 h-full bg-gray-100 p-4 rounded-lg overflow-y-auto"):
                            ui.label("文档目录").classes("text-xl font-bold mb-4")
                            for level, title in titles:
                                ui.link(title, f'#toc-{title.lower().replace(" ", "-")}').classes(
                                    title_css.get(level, defualt_title_css))

                        # 中间内容区域
                        # .classes("custom-hide-scrollbar")
                        with ui.column().classes("w-3/5 h-full overflow-x-auto"):
                            # 设置为 flex justify-center items-center h-screen，其中 h-screen 似乎自动添加 overflow-auto？
                            # fixme: 暂且以这种方式让其居中显示
                            ui.markdown(markdown_content).classes("prose max-w-none").style("width:100%")

                        # 右侧目录
                        # todo: hidden sm:block 这个 @media 媒体模式不知道为什么没什么效果
                        with ui.column().classes(
                                "w-1/6 h-full bg-gray-50 p-4 rounded-lg overflow-y-auto"):
                            ui.label("页面导航").classes("text-xl font-bold mb-4")
                            ui.html(toc_html).classes("toc-container")

                create_moreitems_panel()
            with ui.tab_panel(self.tabs["宠物增强"]):
                # todo: 添加一个下载 excel 的按钮
                # ui.button('Logo', on_click=lambda: ui.download('https://nicegui.io/logo.png'))
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
    with ui.label('Mountains...'):
        with ui.tooltip().classes('bg-transparent'):
            ui.image('/static/logo.jpg').classes('w-64')

    with ui.element().tooltip('...with a tooltip!'):
        ui.html('This is <u>HTML</u>...')


# 使本地目录在指定的端点可用，这对于向前端提供本地数据（如图像）非常有用
# todo: 是否需要处理缓存问题，这每次传送这么多静态资源的话？
app.add_static_files("/static", "./static")

if __name__ == '__main__':
    # todo: 注意，感觉想要使用 nicegui 模仿各自页面，还是需要去系统学习 html css，尤其 css
    ui.run(title=TITLE, favicon="🌿", host="localhost", port=15001, dark=False, reload=False, show=False)
