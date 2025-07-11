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
from datetime import datetime

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

# todo: 设置 logger 的 level，与 settings.DEBUG 对齐

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
                    switch = ui.switch(on_change=lambda e: ui.dark_mode(e.value))  # todo: .tooltip()
                    if not settings.DEBUG:
                        switch.classes("hidden")
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
                    "w-2/3 mx-auto h-full shadow-lg hover:shadow-xl transition-shadow duration-300"):
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

        # 预声明
        # todo: 但是这导致每次跳转会跳到这里，而不是初始化的地方，需要解决
        # todo: 能否在非 __init__ 中定义的属性都警告啊？
        self.header: Optional[ui.header] = None
        self.nav_tabs: Optional[ui.tabs] = None
        self.tabs: Optional[Dict[str, ui.tab]] = None
        self.nav_tabs_panels: Optional[ui.tab_panels] = None

        ui.add_css(utils.read_static_file("./index.css"))

        # 定义，避免重复创建
        self.dark = ui.dark_mode()
        self.update_log_dialog = self.UpdateLogDialog()

        # 初始化页面结构
        self._create_header()
        self._create_content()
        self._create_footer()

        # 页面初始化后
        self.current_nav_tab = self.tabs[app.storage.user.get("nav_tabs:tab_name", "主页")]

        # 注册定时器
        self._register_timers()

        # 注册事件
        self._register_events()

    def _register_timers(self):
        """统一注册计时器"""

        if settings.DEBUG:
            # ui.timer(2, lambda: setattr(self, "current_nav_tab", self.tabs["更多物品"]), once=True)
            pass

        # todo: 练习一下，加载完弹出一个公告 dialog

        # todo: 需要记住客户端的信息，比如现在在哪个 tab，加载完成后，定位到哪里！至于客户端信息，建议只需要单纯 k:v

    def _register_events(self):
        """统一注册事件"""

        def handle_nav_tabs_value_change(args: ValueChangeEventArguments):
            # 记录用户当前所属 tab 页，用于加载时切换

            tab_name = args.value
            if isinstance(tab_name, ui.tab):
                tab_name = args.value._props["name"]  # noqa: Access to a protected member _props of a class

            # logger.debug("{} - {}", args, args.value)
            # logger.debug("nav_tabs 切换，记录当前 tab name：{}", tab_name)
            # null, number, string, list, dict
            app.storage.user["nav_tabs:tab_name"] = tab_name

        # 监听 self.nav_tabs:ui.tabs 值切换
        self.nav_tabs.on_value_change(handle_nav_tabs_value_change)

    def _create_header(self):
        self.header = self.Header([
            "主页",
            *[e["name"] for e in self.controller.get_mod_infos()],
            "更新日志",
            "错误反馈",
        ])

        # 临时兼容
        self.nav_tabs = self.header.nav_tabs
        self.tabs = self.header.tabs

    def _create_home_panel(self):
        with ui.tab_panel(self.tabs["主页"]).classes("w-full justify-center items-center"):
            ui.label("饥荒模组合集").classes("md:mx-auto text-h4")

            with ui.grid().classes("w-full gap-y-8 grid-cols-1 sm:grid-cols-2 xl:grid-cols-3"):
                for mod in self.controller.get_mod_infos():
                    card = self.ModInfoCard(mod)
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

    def _create_error_feedback_panel_v0(self):
        with ui.tab_panel(self.tabs["错误反馈"]):
            # todo: 实现一个表单
            # 表单结构：
            # 反馈人联系方式
            # 错误原因
            # ...
            with ui.card().classes("mx-auto"):
                with ui.grid(columns=2):
                    ui.label("错误原因：")
                    ui.textarea(placeholder="请输入错误原因")

                    ui.label("你的联系方式：")
                    ui.input(placeholder="请输入你的联系方式")

                    ui.label("附件上传：")
                    ui.upload()

                    ui.space()
                    ui.button("提交").classes("justify-end")

    def _create_error_feedback_panel(self):
        with ui.tab_panel(self.tabs["错误反馈"]):
            def submit_form():
                # 表单验证
                if not error_scenario.value:
                    ui.notify("请填写错误场景！", type='negative')
                    return
                if not contact.value:
                    ui.notify("请填写联系方式！", type='negative')
                    return
                if not contact.value.strip().isprintable():
                    ui.notify("联系方式包含非法字符！", type='negative')
                    return
                # 处理文件上传
                file_info = []
                if upload.files:
                    for file in upload.files:
                        file_info.append({
                            'name': file.name,
                            'size': f"{len(file.content) / 1024:.1f} KB",
                            'type': file.type
                        })

                # 在实际应用中，这里可以添加发送邮件/保存到数据库等操作
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 显示提交成功信息
                with dialog:
                    ui.label("反馈提交成功！").classes("text-h6 text-green")
                    ui.label(f"提交时间: {timestamp}")
                    ui.label(f"错误原因: {error_scenario.value}")
                    ui.label(f"联系方式: {contact.value}")

                    if file_info:
                        ui.label("上传附件:")
                        for info in file_info:
                            ui.label(f"· {info['name']} ({info['size']}, {info['type']})")

                    ui.button("关闭", on_click=dialog.close).classes("mt-4")

                dialog.open()

            with ui.card().classes("w-full max-w-3xl mx-auto p-8 shadow-lg rounded-lg"):
                ui.label("错误反馈表单").classes("text-h4 text-primary mb-6 mx-auto")

                # 错误场景 (多行文本)
                ui.label("错误场景：").classes("text-lg font-medium")
                error_scenario = ui.textarea(label="请详细描述遇到的问题",
                                             placeholder="例如：装备某件物品时游戏崩溃...").classes("w-full").props(
                    "outlined")

                # 联系方式
                ui.label("联系方式：").classes("text-lg font-medium mt-6")
                contact = ui.input(label="QQ", placeholder="请输入您的QQ号码").classes("w-full").props("outlined")

                # 文件上传
                # todo: 关于安全问题，需要检测文件上传上限
                #       比如：某个指定的目录存放上传的文件，每次上传并存储文件后，将把目录下的 .size 文件更新，
                #       每次上传也会读取
                # todo: 需要解决 ui.upload 上传后表单未提交的情况，为此，需要唯一标识啊，或者有无什么解决办法？
                ui.label("附件上传：").classes("text-lg font-medium mt-6")
                with ui.column().classes("w-full items-stretch"):
                    upload = ui.upload(
                        label="选择文件",
                        multiple=True,
                        max_file_size=10 * 1024 * 1024,  # 10MB限制
                        auto_upload=True,
                        on_rejected=lambda e: ui.notify(f"文件 {e.name} 超过大小限制 (最大10MB)", type='negative')
                    ).classes("w-full")
                    ui.label("支持上传日志文件、截图等 (最多5个文件，每个文件不超过10MB)").classes(
                        "text-sm text-gray-600 mt-1")

                # 提交按钮
                with ui.row().classes("w-full justify-end"):
                    ui.button("提交反馈", on_click=submit_form, icon="send").classes("mt-8 bg-blue-600 text-white")

            # 创建提交结果对话框
            dialog = ui.dialog().classes("max-w-2xl")

    def _create_content(self):
        with ui.tab_panels(self.nav_tabs).classes("w-full") as self.nav_tabs_panels:
            self.nav_tabs_panels.bind_value(self, "current_nav_tab")

            self._create_home_panel()
            # todo: 左侧目录栏是有必要实现的，右侧可以选择不需要，要不添加一个单纯的活动式菜单栏？点击可以缩小成一个按钮。
            self.MarkdownTabPanel(self.tabs["更多物品"], "./更多物品.md")
            self.MarkdownTabPanel(self.tabs["宠物增强"], "./宠物增强.md")
            self.MarkdownTabPanel(self.tabs["复活按钮和传送按钮"], "./复活按钮和传送按钮.md")
            self.MarkdownTabPanel(self.tabs["便携大箱子"], "./便携大箱子.md")
            self._create_update_log_panel()
            self._create_error_feedback_panel()

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
    from datetime import datetime
    import time

    # 表单提交处理函数
    def submit_form():
        # 表单验证
        if not error_type.value:
            ui.notify('请选择错误类型!', color='negative')
            return
        if not description.value.strip():
            ui.notify('请填写错误描述!', color='negative')
            return
        if not contact.value.strip():
            ui.notify('请填写联系方式!', color='negative')
            return
        if not agree.value:
            ui.notify('请同意隐私条款!', color='negative')
            return

        # 显示提交中状态
        submit_button.text = '提交中...'
        submit_button.disable()

        # 模拟提交过程
        time.sleep(1.5)

        # 显示成功信息
        ui.notify('反馈提交成功! 感谢您的支持!', color='positive', icon='check_circle')

        # 重置表单
        error_type.value = ''
        description.value = ''
        contact.value = ''
        agree.value = False

        # 恢复按钮状态
        submit_button.text = '提交反馈'
        submit_button.enable()

        # 显示提交时间
        timestamp.text = f'最后提交时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        # 显示感谢信息
        with ui.dialog() as dialog, ui.card():
            ui.label('🎉 感谢您的反馈!').classes('text-2xl font-bold text-green-600')
            ui.label('我们的技术团队将尽快处理您的问题')
            ui.label('如需进一步沟通，我们将通过您提供的联系方式与您联系')
            ui.button('关闭', on_click=dialog.close).props('flat color=primary')
        dialog.open()

    # 页面标题
    ui.page_title('错误反馈系统')

    # 页面头部
    with ui.header(elevated=True).style('background-color: #2563eb').classes('items-center justify-between'):
        ui.label('错误反馈系统').classes('text-2xl font-bold text-white')
        with ui.row():
            ui.button('首页', icon='home').props('flat color=white')
            ui.button('帮助', icon='help').props('flat color=white')
            ui.button('关于', icon='info').props('flat color=white')

    # todo: 往下偏移
    # 主要内容区域
    with ui.row().classes('w-full max-w-7xl mx-auto p-4'):
        # 左侧介绍区域
        # w-1/4 w-3/4 不行，必须 w-2/3 ...

        # todo: 居中
        with ui.column().classes('w-1/4'):
            ui.label('问题反馈说明').classes('text-xl font-bold text-blue-800 mb-4')
            ui.markdown('''
            **请提供以下信息帮助我解决问题：**

            1. 详细描述问题现象
            2. 提供您的联系方式
            3. 上传相关文件（可选）

            ''').classes('text-gray-700 mb-4')

            ui.separator().classes('my-4')

            with ui.column().classes('bg-blue-50 p-4 rounded-lg'):
                ui.label('反馈小贴士').classes('text-lg font-bold text-blue-700 mb-2')
                ui.markdown('''
                - 尽可能详细描述问题重现步骤
                - 提供截图或日志文件有助于快速定位问题
                - 留下有效的联系方式以便我们与您沟通
                - 紧急问题可添加QQ群: 592159151
                ''')

        # 右侧表单区域
        with ui.column().classes('w-2/3 bg-white shadow-lg rounded-lg p-6'):
            ui.label('错误反馈表单').classes('text-2xl font-bold text-gray-800 mb-6 mx-auto')

            # 错误描述
            ui.label('错误描述 *').classes('text-sm font-medium text-gray-700 mb-1')
            description = ui.textarea(
                label='请详细描述错误现象、重现步骤等',
                placeholder='例如：当穿戴某件物品的时候...'
            ).classes('w-full mb-4').props('outlined autogrow')

            # 联系方式
            ui.label('联系方式 *').classes('text-sm font-medium text-gray-700 mb-1')
            contact = ui.input(
                label='邮箱/电话',
                placeholder='请输入您的邮箱或手机号码'
            ).classes('w-full mb-4').props('outlined')

            # 附件上传
            ui.label('上传附件').classes('text-sm font-medium text-gray-700 mb-1')
            with ui.column().classes(
                    'w-full mb-4 border border-dashed border-gray-300 rounded-lg p-4 items-center'):
                ui.icon('cloud_upload', size='lg').classes('text-blue-500 mb-2')
                ui.label('点击或拖拽文件到此处上传').classes('text-gray-500')
                ui.upload(
                    label='选择文件',
                    multiple=True,
                    auto_upload=True,
                    on_upload=lambda e: ui.notify(f'已上传: {e.name}')
                ).props('accept=".jpg,.jpeg,.png,.log,.txt"').classes('mt-2')
                ui.label('支持格式: JPG, PNG, LOG, TXT (最大10MB)').classes('text-xs text-gray-400 mt-2')

            # 提交按钮
            with ui.row().classes("w-full justify-end"):
                submit_button = ui.button('提交反馈', on_click=submit_form, icon='send') \
                    .classes(
                    'bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-md transition duration-300') \
                    .props('no-caps')

            # 提交时间显示
            timestamp = ui.label('').classes('text-xs text-gray-500 mt-2 text-right')

    # 页脚
    with ui.footer().style('background-color: #f3f4f6').classes('text-center p-4 text-gray-600'):
        ui.label('© 2023 技术支持中心 | 错误反馈系统 v1.0').classes('text-sm')
        ui.label('服务时间: 周一至周五 9:00-18:00').classes('text-xs mt-1')


# 使本地目录在指定的端点可用，这对于向前端提供本地数据（如图像）非常有用
# todo: 是否需要处理缓存问题，这每次传送这么多静态资源的话？
# app.mount('/static', WhiteNoise(directory=str(STATIC_DIR), max_age=600))
app.add_static_files("/static", "./static")

if __name__ == '__main__':
    # todo: 注意，感觉想要使用 nicegui 模仿各自页面，还是需要去系统学习 html css，尤其 css
    ui.run(title=TITLE, favicon="🌿", host="localhost", port=15001, dark=False, reload=False, show=False,
           on_air=os.getenv("NICEGUI_TOKEN"), storage_secret="NOSET")
