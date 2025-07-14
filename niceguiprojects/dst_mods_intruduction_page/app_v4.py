"""
### 总结
1. 作为半吊子 nicegui 前端开发，多个版本是正常的，但是我发现，之前版本的代码编写将让你对页面结构更清晰，
   这意味着，如果你重新描述一下你的页面结构给 ai，他很有可能能够提供不错的回答！！！

"""

import functools
import os
import re
import shutil
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union, Optional, Tuple

import cachetools
from asgiref.sync import sync_to_async
from dotenv import load_dotenv
from loguru import logger

from nicegui import ui, app
from nicegui.elements.tabs import Tab
from nicegui.events import ValueChangeEventArguments, UploadEventArguments

import nicegui_settings
import utils
from nicegui_settings import STATIC_DIR
from djangoorm import load_djangoorm
from djangoorm.app import models

load_dotenv()
load_djangoorm()

# todo: 设置 logger 的 level，与 settings.DEBUG 对齐
#       我认为暂且不需要，
#       但是 logger 信息最好设置成文件一份控制台一份，哪怕一模一样！

# todo: 确定此处的作用（效果：所有 ExceptionGroup 会被简化为单行错误提示，其他标准异常仍会显示完整堆栈）
# if sys.version_info >= (3, 11):
#     sys.excepthook = lambda t, v, tb: print(f"Error: {v}")

# Mock
models.ModInfo.mock_init_data()


# todo: 我想知道 nicegui 或者说前端开发的文件结构如何，但是目前我认为不管怎么样，按照自己的理解去做吧！


class Helper:
    @staticmethod
    def get_update_log_mardown_files():  # todo:  -> Generator[str] 如何使用？
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
    class _create_header_element(ui.header):  # noqa: Class names should use CapWords convention
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
                    if not nicegui_settings.DEBUG:
                        switch.classes("hidden")
                with ui.row().classes("w-full bg-green-500 text-white"):
                    with ui.tabs().classes("w-full") as self.nav_tabs:
                        logger.info("header tab_names: {}", tab_names)
                        for tab_name in tab_names:
                            self.tabs[tab_name] = ui.tab(tab_name)

    class _create_mod_info_card(ui.card):  # noqa: Class names should use CapWords convention
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

    class _create_update_log_dialog(ui.dialog):  # noqa: Class names should use CapWords convention
        """提供给更新日志模块使用的弹窗"""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            with self, ui.card():
                self.content_markdown = ui.markdown()

    class _create_markdown_tab_panel(ui.tab_panel):  # noqa: Class names should use CapWords convention
        class _create_search_input_card(ui.card):  # noqa: Class names should use CapWords convention
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                with self.classes("""
                w-full max-w-2xl mx-auto my-8 p-4 shadow-lg rounded-xl bg-white dark:bg-gray-800 transition-all
                """):
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
                markdown_content = self._read_markdown_file(doc_path)

                # 使用响应式容器
                with ui.column().classes("w-full flex justify-center items-center p-4 gap-y-0"):
                    # todo: 推荐加到 ui.header 里，直接复用 ctrl+F，凑活吧！
                    # self._create_search_input_card()

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
        def _read_markdown_file(relative_path: str) -> str:
            filepath = STATIC_DIR / "markdown" / relative_path
            if not filepath.exists():
                return """文档不存在"""
            return filepath.read_text("utf-8")

    class _create_error_feedback_panel(ui.tab_panel):  # noqa: Class names should use CapWords convention
        def _create_file_upload_component(self) -> ui.upload:
            """创建文件上传相关组件"""

            def _handle_upload(e: UploadEventArguments):
                logger.debug("[on_upload] name: {}, type: {}", e.name, e.type)
                filepath = file_upload_manager.save(e.content.read(),
                                                    os.path.splitext(e.name)[1],
                                                    is_temp=True,
                                                    ret_relative_path=True)
                self._uploaded_files.append(filepath)

            file_upload_manager = utils.FileUploadManager()

            # fixme: 文件上传相关逻辑待定
            # 文件上传
            # todo: 关于安全问题，需要检测文件上传上限
            #       比如：某个指定的目录存放上传的文件，每次上传并存储文件后，将把目录下的 .size 文件更新，
            #       每次上传也会读取
            # todo: 需要解决 ui.upload 上传后表单未提交的情况，为此，需要唯一标识啊，或者有无什么解决办法？
            with ui.column().classes("w-full items-stretch"):
                upload = ui.upload(
                    label="选择文件",
                    multiple=True,
                    on_upload=_handle_upload,
                    max_file_size=10 * 1024 * 1024,  # 10MB限制
                    auto_upload=True,  # 自动上传
                    on_rejected=lambda e: ui.notify(f"文件超过大小限制 (最大10MB)", type='negative')
                ).classes("w-full")
                ui.label("支持上传日志文件、截图等 (最多5个文件，每个文件不超过10MB)").classes(
                    "text-sm text-gray-600 mt-1")
            return upload

        def __init__(self, name: Union[Tab, str]) -> None:
            super().__init__(name)

            # todo: 存相对路径！
            self._uploaded_files: List[Path] = []

            # 预声明

            # 创建提交结果对话框
            self._dialog = ui.dialog().classes("max-w-2xl")

            self._error_scenario, self._contact, self._upload = self._build_ui()

        def _rebuild(self):
            self.clear()
            self._error_scenario, self._contact, self._upload = self._build_ui()

        def _build_ui(self) -> Tuple[ui.textarea, ui.input, ui.upload]:
            with self, ui.card().classes("w-full max-w-3xl mx-auto p-8 shadow-lg rounded-lg"):
                ui.label("错误反馈表单").classes("text-h4 text-primary mb-6 mx-auto")

                ui.label("错误场景：").classes("text-lg font-medium")
                error_scenario = ui.textarea(label="请详细描述遇到的问题",
                                             placeholder="例如：装备某件物品时游戏崩溃...").classes(
                    "w-full").props(
                    "outlined")

                ui.label("联系方式：").classes("text-lg font-medium mt-6")
                contact = ui.input(label="QQ号码", placeholder="请输入您的QQ号码",
                                   validation=self._contact_validation).classes("w-full").props("outlined")

                ui.label("附件上传：").classes("text-lg font-medium mt-6")
                upload = self._create_file_upload_component()

                with ui.row().classes("w-full justify-end"):
                    ui.button("提交反馈", on_click=lambda: self._submit_form(), icon="send").classes(
                        "mt-8 bg-blue-600 text-white")

            return error_scenario, contact, upload

        @property
        def _contact_validation(self):
            def _is_valid_qq_logic(qq_number: str) -> bool:
                """通过逻辑判断校验QQ号码"""
                # 检查是否为纯数字且长度合法
                if not qq_number.isdigit() or len(qq_number) < 5 or len(qq_number) > 12:
                    return False
                # 检查首位是否为0
                if qq_number[0] == '0':
                    return False
                return True

            return {"请输入正确格式的QQ号码": _is_valid_qq_logic}

        async def _submit_form(self):
            logger.debug("提交表单")
            try:
                # 校验表单内容，要求错误场景和联系方式必填
                # todo: 需要实现动态效果，Schema 库应该也可以使用的
                if not self._error_scenario.value:
                    ui.notify("错误场景为必填项", type="positive")
                    return

                if not self._contact.value:
                    ui.notify("联系方式为必填项", type="negative")
                    return

                # todo: self._contact 的 validation 也需要满足啊
                for error_msg, check in self._contact.validation.items():
                    if not check(self._contact.value):
                        ui.notify(f"联系方式不满足校验：{error_msg}", type="negative")
                        return

                # 在实际应用中，这里可以添加发送邮件/保存到数据库等操作
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                logger.debug("self._uploaded_files: {}", self._uploaded_files)

                # 显示提交成功信息
                # fixme: 无法显示，不止为何
                self._dialog.clear()
                with self._dialog:
                    ui.label("反馈提交成功！").classes("text-h6 text-green")
                    ui.label(f"提交时间: {timestamp}")
                    ui.label(f"错误原因: {self._error_scenario.value}")
                    ui.label(f"联系方式: {self._contact.value}")

                    ui.button("关闭", on_click=self._dialog.close).classes("mt-4")

                self._dialog.open()

                # 存储数据至数据库中
                # （前后端就是相辅相成，后端数据库表决定前端，但是前端也决定后端，虽然全部都由需求决定）
                await models.ErrorFeedbackInfo.objects.acreate(**dict(
                    error_scenario=self._error_scenario.value,
                    contact=self._contact.value,
                    filepaths=[str(e) for e in self._uploaded_files]
                ))
            except Exception as e:
                logger.error(f"{e}\n{traceback.format_exc()}")
                ui.notify(f"出现出乎意料的操作，请联系开发人员（当前时间：{datetime.now()}）", type="negative")
            else:
                ui.notify("错误反馈成功！", type="positive")

                # fixme: 此处又出错了怎么办？嵌套出错还得套个异常吗？还是说加个全局异常即可。
                # 将上传的文件从临时目录转移至实际的目录
                # assert 相对路径
                for filepath in self._uploaded_files:
                    shutil.move(utils.FileUploadManager.TEMP_STORAGE_PATH / filepath,
                                utils.FileUploadManager.STORAGE_PATH / filepath)
                    logger.debug("将文件 {} 从临时目录移动至实际目录", filepath)
                self._uploaded_files.clear()

                self._rebuild()

    def __init__(self, mod_infos):
        self._controller = Controller()
        self._mod_infos = mod_infos

        # todo: 是否需要预声明？
        # todo: 但是这导致每次跳转会跳到这里，而不是初始化的地方，需要解决
        # todo: 能否在非 __init__ 中定义的属性都警告啊？
        # self.header: Optional[ui.header] = None
        # self.nav_tabs: Optional[ui.tabs] = None
        # self.tabs: Optional[Dict[str, ui.tab]] = None
        # self.nav_tabs_panels: Optional[ui.tab_panels] = None

        # 初始化页面结构
        ui.add_css(utils.read_static_file("./index.css"))

        self._dark = ui.dark_mode()
        self._update_log_dialog = self._create_update_log_dialog()
        self._create_header()
        self._create_content()
        self._create_footer()

        # 页面初始化后
        self._current_nav_tab = self._header.tabs[app.storage.user.get("nav_tabs:tab_name", "主页")]

        # 注册定时器
        self._register_timers()

        # 注册事件
        self._register_events()

    def _register_timers(self):
        """统一注册计时器"""

        if nicegui_settings.DEBUG:
            # ui.timer(2, lambda: setattr(self, "_current_nav_tab", self.tabs["更多物品"]), once=True)
            pass

        # todo: 练习一下，加载完弹出一个公告 dialog

        # todo: 需要记住客户端的信息，比如现在在哪个 tab，加载完成后，定位到哪里！至于客户端信息，建议只需要单纯 k:v

    def _register_events(self):
        """统一注册事件"""

        def _handle_nav_tabs_value_change(args: ValueChangeEventArguments):
            # 记录用户当前所属 tab 页，用于加载时切换

            tab_name = args.value
            if isinstance(tab_name, ui.tab):
                tab_name = args.value._props["name"]  # noqa: Access to a protected member _props of a class

            # logger.debug("{} - {}", args, args.value)
            # logger.debug("nav_tabs 切换，记录当前 tab name：{}", tab_name)
            # null, number, string, list, dict
            app.storage.user["nav_tabs:tab_name"] = tab_name

        # 监听 self.nav_tabs:ui.tabs 值切换
        self._header.nav_tabs.on_value_change(_handle_nav_tabs_value_change)

        def _handle_connect():
            last_timestamp_key = "index:visitor_count:last_timestamp"
            value_key = "index:visitor_count:value"
            last_timestamp = app.storage.general.get(last_timestamp_key)
            # 【亮点】处理防抖：5s 内重复刷新不记录（改进：引入 redis 实现）
            if (last_timestamp is None) or (time.time() > last_timestamp + 5):
                app.storage.general[last_timestamp_key] = time.time()
                app.storage.general[value_key] = app.storage.general.get(value_key, 0) + 1

            self._visitor_count.set_text(str(app.storage.general[value_key]))

        # 监听客户端连接
        app.on_connect(_handle_connect)

    def _create_header(self):
        self._header = self._create_header_element([
            "主页",
            *[e["name"] for e in self._mod_infos],
            "更新日志",
            "错误反馈",
        ])

    def _create_content(self):
        with ui.tab_panels(self._header.nav_tabs).classes("w-full") as self._nav_tabs_panels:
            self._nav_tabs_panels.bind_value(self, "_current_nav_tab")

            self._create_home_panel(self._header.tabs["主页"])

            # todo: 左侧目录栏是有必要实现的，右侧可以选择不需要，要不添加一个单纯的活动式菜单栏？点击可以缩小成一个按钮。
            self._create_markdown_tab_panel(self._header.tabs["更多物品"], "./更多物品.md")
            self._create_markdown_tab_panel(self._header.tabs["宠物增强"], "./宠物增强.md")
            self._create_markdown_tab_panel(self._header.tabs["复活按钮和传送按钮"], "./复活按钮和传送按钮.md")
            self._create_markdown_tab_panel(self._header.tabs["便携大箱子"], "./便携大箱子.md")

            self._create_update_log_panel(self._header.tabs["更新日志"])
            self._create_error_feedback_panel(self._header.tabs["错误反馈"])

    def _create_footer(self):
        # todo: 暂且计划是加一个不算明显的 footer，用于记录一些信息，比如点击量，访问量等
        with ui.footer().classes("w-full justify-end") as footer:
            footer.tailwind.background_color("white")
            with ui.row():
                ui.icon("eye")
                self._visitor_count = ui.label()
                # todo: 这个 tooltip 有些小问题
                self._visitor_count.tooltip("访问量")
                self._visitor_count.tailwind.text_color("green-300").font_weight("normal")

    def _create_home_panel(self, tab: ui.tab):
        with ui.tab_panel(tab).classes("w-full justify-center items-center"):
            ui.label("饥荒模组合集").classes("md:mx-auto text-h4")

            with ui.grid().classes("w-full gap-y-8 grid-cols-1 sm:grid-cols-2 xl:grid-cols-3"):
                for mod in self._mod_infos:
                    card = self._create_mod_info_card(mod)
                    card.on("click", functools.partial(
                        lambda mod, e: self._header.nav_tabs.set_value(self._header.tabs[mod["name"]]), mod))

    def _create_update_log_panel(self, tab: ui.tab):
        with ui.tab_panel(tab).classes("w-full"):
            with ui.column().classes("w-full gap-y-4"):
                for filename, content in Helper.get_update_log_mardown_files():
                    # todo: 优化 card 及其内部 markdown
                    with ui.card().classes("w-full h-80 overflow-auto"):
                        with ui.row():  # todo: 让其中的元素居于中轴
                            # https://quasar.dev/vue-components/spinners#qspinner-api
                            ui.spinner("ball", size="lg", color="green")

                            with ui.column().classes("pt-2"):
                                # 点击弹出弹窗展示内容
                                title = ui.label(f"{filename[:-3]}")
                                title.tooltip("点击预览")
                                title.classes("cursor-pointer hover:text-blue-500 text-1xl md:text-2xl")
                                title.tailwind.text_color("black").font_weight("bold")
                                # click | dblclick
                                title.on("click", functools.partial(lambda content: (
                                    logger.debug("[update-log] title click"),
                                    self._update_log_dialog.content_markdown.set_content(content),
                                    self._update_log_dialog.open()
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
    pass


# 使本地目录在指定的端点可用，这对于向前端提供本地数据（如图像）非常有用
# todo: 是否需要处理缓存问题，这每次传送这么多静态资源的话？
# app.mount('/static', WhiteNoise(directory=str(STATIC_DIR), max_age=600))
app.add_static_files("/static", "./static")

if __name__ == '__main__':
    # app.on_startup(_handle_startup)

    # todo: 注意，感觉想要使用 nicegui 模仿各自页面，还是需要去系统学习 html css，尤其 css
    ui.run(title=nicegui_settings.TITLE,
           favicon=nicegui_settings.FAVICON,
           host=nicegui_settings.HOST,
           port=nicegui_settings.PORT,
           dark=False,
           reload=False,
           show=False,
           on_air=os.getenv("NICEGUI_TOKEN"),
           storage_secret="NOSET")
