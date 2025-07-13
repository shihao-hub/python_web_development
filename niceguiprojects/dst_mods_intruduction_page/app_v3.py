"""
### 总结
1. 作为半吊子 nicegui 前端开发，多个版本是正常的，但是我发现，之前版本的代码编写将让你对页面结构更清晰，
   这意味着，如果你重新描述一下你的页面结构给 ai，他很有可能能够提供不错的回答！！！

"""

import asyncio
import functools
import json
import os
import re
import random
import traceback
import uuid
from abc import abstractmethod, ABC
from datetime import datetime

from typing_extensions import override
from pathlib import Path
from typing import Optional, Literal, Dict, Generator, List, Union

import markdown
import cachetools
from asgiref.sync import sync_to_async, async_to_sync
from loguru import logger
from markdown.extensions.toc import TocExtension
from whitenoise import WhiteNoise
from dotenv import load_dotenv

from nicegui import ui, app
from nicegui.events import Handler, ValueChangeEventArguments, UploadEventArguments
from nicegui.elements.tabs import Tab

import settings
import utils
from settings import STATIC_DIR, ROOT_DIR
from djangoorm import load_djangoorm
from djangoorm.app import models

load_dotenv()
load_djangoorm()

# todo: 设置 logger 的 level，与 settings.DEBUG 对齐

TITLE = "心悦卿兮的饥荒模组合集"

# Mock
models.ModInfo.mock_init_data()


class Helper:

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
            # todo: 为什么 open file 这个操作，不会提示不允许在异步中执行？
            yield filename, utils.read_markdown_file(filename)


class Controller:
    """
    1. 暂且视其为 django 的 View/Response
    2. 此处由 nicegui 调用，因此必须是 async 形式
    """

    def __init__(self):
        pass

    async def get_mod_item_infos(self, mod_name="更多物品"):
        """获得指定模组物品的信息"""
        raise NotImplemented


class View:
    class Header(ui.header):  # 无普遍性
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
        class SearchInputCard(ui.card):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                with self.classes(
                        "w-full max-w-2xl mx-auto my-8 p-4 shadow-lg rounded-xl bg-white dark:bg-gray-800 transition-all"):
                    with ui.row().classes("w-full items-center gap-2 flex-wrap"):
                        # 搜索图标
                        ui.icon("search").classes("text-gray-500 dark:text-gray-400 shrink-0")

                        # 搜索输入框
                        self.search_input = ui.input(placeholder="搜索内容...").classes("""
                            flex-grow bg-gray-50 dark:bg-gray-700 rounded-lg
                            px-4 py-2 text-gray-800 dark:text-gray-200
                            focus:outline-none focus:ring-2 focus:ring-blue-500
                            transition-all duration-300
                        """).props("standout dense").on("keydown.enter", self.trigger_search)

                        # 搜索按钮
                        ui.button("搜索", on_click=self.trigger_search, icon="search").classes(
                            "bg-blue-500 hover:bg-blue-600 text-white"
                        ).props("dense")

                        # 帮助提示按钮
                        with ui.button(icon="help_outline").props("flat dense").classes(
                                "text-gray-500 dark:text-gray-400"):
                            with ui.tooltip().classes("max-w-xs"):
                                ui.markdown("""
                                **搜索提示:**
                                - 按 `Enter` 键或点击搜索按钮进行搜索
                                - 按 `Ctrl+F` 激活浏览器原生搜索功能
                                - 按 `Esc` 键清除搜索内容
                                """)

                        # 快捷键提示
                        ui.label().classes("text-xs text-gray-500 dark:text-gray-400 ml-2 hidden sm:block").set_text(
                            "Ctrl+F")

                    # 搜索选项行
                    with ui.row().classes("w-full mt-3 justify-between items-center gap-4 flex-wrap"):
                        with ui.row().classes("items-center gap-3"):
                            # 搜索选项
                            ui.toggle(["标题", "内容", "标签"], value="内容").props("dense").bind_value(self,
                                                                                                        "search_type")
                            ui.checkbox("区分大小写").bind_value(self, "case_sensitive")

                        # 搜索结果统计
                        self.result_label = ui.label().classes("text-sm text-gray-600 dark:text-gray-300")

                        # 清空按钮
                        ui.button("清空", on_click=self.clear_search, icon="clear").classes(
                            "text-gray-500 hover:text-red-500"
                        ).props("flat dense").bind_visibility_from(self.search_input, "value", lambda v: bool(v))

            def trigger_search(self):
                """触发搜索功能"""
                search_text = self.search_input.value.strip()
                if not search_text:
                    ui.notify("请输入搜索内容", type="warning")
                    return

                # 在这里添加您的实际搜索逻辑
                ui.notify(f"正在搜索: {search_text}")

                # 更新结果统计
                self.result_label.set_text(f"找到 25 个相关结果")

                # 激活浏览器搜索（模拟 Ctrl+F）
                self.activate_browser_search(search_text)

            def clear_search(self):
                """清空搜索内容"""
                self.search_input.value = ""
                self.result_label.set_text("")
                ui.notify("已清除搜索内容", type="positive")

                # 清除浏览器搜索高亮
                self.clear_browser_search()

            def activate_browser_search(self, text):
                """激活浏览器原生搜索功能"""
                # 使用 JavaScript 模拟 Ctrl+F 并填充搜索词
                js_code = f"""
                    // 尝试激活浏览器的查找功能
                    try {{
                        // 创建一个自定义事件模拟 Ctrl+F
                        const event = new KeyboardEvent('keydown', {{
                            key: 'f',
                            ctrlKey: true,
                            bubbles: true,
                            cancelable: true
                        }});

                        // 触发事件
                        document.dispatchEvent(event);

                        // 延迟填充搜索框（浏览器需要时间打开搜索栏）
                        setTimeout(() => {{
                            // 尝试找到浏览器的搜索框并填充内容
                            const searchInputs = document.querySelectorAll('input[type="search"], input[name="find"]');
                            if (searchInputs.length > 0) {{
                                searchInputs[0].value = '{text}';
                                searchInputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                            }} else {{
                                // 如果找不到搜索框，使用 window.find 方法
                                window.find('{text}');
                            }}
                        }}, 300);
                    }} catch (e) {{
                        console.error('激活浏览器搜索失败:', e);
                        // 回退到 window.find 方法
                        window.find('{text}');
                    }}
                """
                ui.run_javascript(js_code)

            def clear_browser_search(self):
                """清除浏览器搜索高亮"""
                ui.run_javascript("""
                    // 清除浏览器搜索高亮
                    if (window.getSelection) {
                        window.getSelection().removeAllRanges();
                    }

                    // 尝试清除浏览器搜索框内容
                    const searchInputs = document.querySelectorAll('input[type="search"], input[name="find"]');
                    if (searchInputs.length > 0) {
                        searchInputs[0].value = '';
                        searchInputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                    }
                """)

        def __init__(self, tab: ui.tab, doc_path: str):
            super().__init__(tab)

            with self:
                markdown_content = self.read_markdown_file(doc_path)

                # 使用响应式容器
                with ui.column().classes("w-full flex justify-center items-center p-4 gap-y-0"):
                    # todo: 推荐加到 ui.header 里，直接复用 ctrl+F，凑活吧！
                    # self.SearchInputCard()

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

    class ErrorFeedbackPanel(ui.tab_panel):
        def __init__(self, name: Union[Tab, str]) -> None:
            super().__init__(name)

            self.file_upload_manager = utils.FileUploadManager()
            # todo: 存相对路径！
            self.uploaded_files: List[Path] = []

            with self, ui.card().classes("w-full max-w-3xl mx-auto p-8 shadow-lg rounded-lg"):
                ui.label("错误反馈表单").classes("text-h4 text-primary mb-6 mx-auto")

                # 错误场景 (多行文本)
                ui.label("错误场景：").classes("text-lg font-medium")
                self.error_scenario = ui.textarea(label="请详细描述遇到的问题",
                                                  placeholder="例如：装备某件物品时游戏崩溃...").classes("w-full").props(
                    "outlined")

                # 联系方式
                ui.label("联系方式：").classes("text-lg font-medium mt-6")
                self.contact = ui.input(label="QQ号码", placeholder="请输入您的QQ号码",
                                        validation=self.qq_validation).classes("w-full").props("outlined")

                # 文件上传
                # todo: 关于安全问题，需要检测文件上传上限
                #       比如：某个指定的目录存放上传的文件，每次上传并存储文件后，将把目录下的 .size 文件更新，
                #       每次上传也会读取
                # todo: 需要解决 ui.upload 上传后表单未提交的情况，为此，需要唯一标识啊，或者有无什么解决办法？
                ui.label("附件上传：").classes("text-lg font-medium mt-6")
                with ui.column().classes("w-full items-stretch"):
                    self.upload = ui.upload(
                        label="选择文件",
                        multiple=True,
                        on_upload=self.handle_upload,
                        max_file_size=10 * 1024 * 1024,  # 10MB限制
                        auto_upload=True,  # 自动上传
                        on_rejected=lambda e: ui.notify(f"文件超过大小限制 (最大10MB)", type='negative')
                    ).classes("w-full")
                    ui.label("支持上传日志文件、截图等 (最多5个文件，每个文件不超过10MB)").classes(
                        "text-sm text-gray-600 mt-1")

                # 提交按钮
                with ui.row().classes("w-full justify-end"):
                    ui.button("提交反馈", on_click=lambda: self.submit_form(), icon="send").classes(
                        "mt-8 bg-blue-600 text-white")

                # 创建提交结果对话框
            self.dialog = ui.dialog().classes("max-w-2xl")
            with self.dialog:
                ui.label("Test")

        def _create_ui(self):
            """创建 UI"""
            # todo: 骨架和皮肤只在此处？

        def _register_callbacks(self):
            """注册回调"""
            # todo: 血肉在此处？

        def handle_upload_v0(self, e: UploadEventArguments):
            logger.debug("[on_upload] name: {}, type: {}", e.name, e.type)
            _, extenstion = os.path.splitext(e.name)
            filename = f"{uuid.uuid4()}"
            if extenstion:
                filename = filename + "." + extenstion
            with open(str(settings.UPLOADED_DIR / filename), "wb") as f:
                f.write(e.content.read())

        def handle_upload(self, e: UploadEventArguments):
            logger.debug("[on_upload] name: {}, type: {}", e.name, e.type)
            filepath = self.file_upload_manager.save(e.content.read(), os.path.splitext(e.name)[1])
            self.uploaded_files.append(filepath)

        @property
        def qq_validation(self):
            def is_valid_qq_logic(qq_number: str) -> bool:
                """通过逻辑判断校验QQ号码"""
                # 检查是否为纯数字且长度合法
                if not qq_number.isdigit() or len(qq_number) < 5 or len(qq_number) > 12:
                    return False
                # 检查首位是否为0
                if qq_number[0] == '0':
                    return False
                return True

            return {"请输入正确格式的QQ号码": is_valid_qq_logic}

        async def submit_form(self):
            logger.debug("提交表单")
            try:

                # 在实际应用中，这里可以添加发送邮件/保存到数据库等操作
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                logger.debug("self.uploaded_files: {}", self.uploaded_files)

                # 显示提交成功信息
                # fixme: 无法显示，不止为何
                self.dialog.clear()
                with self.dialog:
                    ui.label("反馈提交成功！").classes("text-h6 text-green")
                    ui.label(f"提交时间: {timestamp}")
                    ui.label(f"错误原因: {self.error_scenario.value}")
                    ui.label(f"联系方式: {self.contact.value}")

                    ui.button("关闭", on_click=self.dialog.close).classes("mt-4")

                self.dialog.open()

                # 存储数据至数据库中
                # （前后端就是相辅相成，后端数据库表决定前端，但是前端也决定后端，虽然全部都由需求决定）
                await models.ErrorFeedbackInfo.objects.acreate(**dict(
                    error_scenario=self.error_scenario.value,
                    contact=self.contact.value,
                    filepaths=[str(e) for e in self.uploaded_files]
                ))
            except Exception as e:
                logger.error(f"{e}\n{traceback.format_exc()}")
                ui.notify(f"出现出乎意料的操作，请联系开发人员（当前时间：{datetime.now()}）", type="negative")
            else:
                ui.notify("错误反馈成功！", type="positive")
                self.uploaded_files.clear()
                logger.info("self.uploaded_files 清除成功！")
                # todo: 清空表单数据

                self.error_scenario.value = ""
                self.error_scenario.update()
                self.contact.value = ""
                self.contact.update()
                self.upload.reset()

                # todo: 用户刷新后数据是否应该存储保证页面展示？
                # todo: 确定一下 self.uploaded_files 是否是每个客户端链接独属的？

    def __init__(self, mod_infos):
        self.controller = Controller()
        self.helper = Helper()
        self.mod_infos = mod_infos

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
            *[e["name"] for e in self.mod_infos],
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
                for mod in self.mod_infos:
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
                for filename, content in self.helper.get_update_log_mardown_files():
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

    def _create_content(self):
        with ui.tab_panels(self.nav_tabs).classes("w-full") as self.nav_tabs_panels:
            self.nav_tabs_panels.bind_value(self, "current_nav_tab")

            # todo: 我想知道 nicegui 或者说前端开发的文件结构如何，但是目前我认为不管怎么样，按照自己的理解去做吧！

            self._create_home_panel()
            # todo: 左侧目录栏是有必要实现的，右侧可以选择不需要，要不添加一个单纯的活动式菜单栏？点击可以缩小成一个按钮。
            self.MarkdownTabPanel(self.tabs["更多物品"], "./更多物品.md")
            self.MarkdownTabPanel(self.tabs["宠物增强"], "./宠物增强.md")
            self.MarkdownTabPanel(self.tabs["复活按钮和传送按钮"], "./复活按钮和传送按钮.md")
            self.MarkdownTabPanel(self.tabs["便携大箱子"], "./便携大箱子.md")
            self._create_update_log_panel()
            self.ErrorFeedbackPanel(self.tabs["错误反馈"])

    def _create_footer(self):
        # todo: 暂且计划是加一个不算明显的 footer，用于记录一些信息，比如点击量，访问量等
        pass


@ui.page("/")
async def page_index():
    # 严格注意此处
    mod_infos = await sync_to_async(lambda: models.ModInfo.objects.filter(is_deleted=False).order_by("id"))()
    View([modinfo.to_dict() async for modinfo in mod_infos])


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
