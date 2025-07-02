from typing import Tuple, Optional

from loguru import logger

from nicegui import ui
from nicegui.events import Handler, UploadEventArguments


class UploadDialog(ui.dialog):
    """用于文件上传的 dialog"""

    def __init__(self,
                 *,
                 value: bool = False,
                 max_file_size: int = 10 * 1024 * 1024,  # 单个文件最大大小
                 accept: Tuple = (".csv", ".xlsx", ".md"),  # 文件上传支持的文件类型
                 on_upload: Optional[Handler[UploadEventArguments]] = None,
                 ) -> None:
        super().__init__(value=value)
        # 使用 w-full max-w-2xl 类使对话框宽度自适应但不超过合理宽度
        # fixme: max-w-2xl 导致 dialog 关闭的时候，右侧大概一半的页面出现分界线
        # 【创建对话框】
        dialog = self.classes("max-w-2xl w-full")

        # 添加 max-h-[70vh] overflow-auto 设置最大高度为视口的70%并添加滚动条
        # 【对话框内容区域】
        # 使用 Tailwind 的 [&>*]:w-full 可以强制所有子元素继承宽度
        with dialog, ui.card().classes("p-6 max-h-[70vh] overflow-auto w-full "
                                       "shadow-xl rounded-lg bg-gradient-to-br "
                                       "from-blue-50 to-indigo-50 [&>*]:w-full"):
            # 【对话框标题区】
            # border-b-2 border-blue-200 给下方添加了一条蓝色横线
            with ui.row().classes("items-center justify-between w-full mb-4 pb-2 border-b-2 border-blue-200"):
                ui.icon("cloud_upload", size="lg", color="primary").classes("text-blue-500")
                ui.label("文件上传").classes("text-xl font-bold text-gray-700")
                ui.button(icon="close", on_click=dialog.close).props("flat dense").classes(
                    "text-gray-500 hover:bg-blue-100")
            # 【上传说明区域】
            with ui.column().classes("bg-blue-100/50 p-4 rounded-lg mb-6 border border-blue-200"):
                ui.markdown("**支持的文件类型**").classes("text-blue-800 font-medium")
                ui.label(f'{", ".join(accept)}').classes("text-sm text-gray-600 mb-2")

                ui.markdown("**文件大小限制**").classes("text-blue-800 font-medium")
                ui.label(f"单个文件最大 {max_file_size / 1024 / 1024:.1f} MB").classes("text-sm text-gray-600")
            # 【文件上传区域】
            with ui.column().classes("border-2 border-dashed border-blue-300 rounded-lg "
                                     "p-8 text-center bg-white hover:bg-blue-50 "
                                     "transition-colors duration-300 mb-6") as upload_area:
                # 拖放区域内容
                ui.icon("cloud_upload", size="xl", color="primary").classes("text-blue-400 mx-auto mb-4")
                ui.label("拖放文件到下方区域或点击上传").classes("text-gray-600 font-medium mb-2")

                def handle_upload(e: UploadEventArguments):
                    if on_upload:
                        return on_upload(e)
                    # 【默认逻辑】
                    logger.debug("上传文件: {}", e),
                    ui.notify("文件上传成功", color="success")
                    # 【涉及业务的逻辑块】
                    # 上传文件成功后，立刻触发前台 loading，最好能够刷新操作进度
                    # 继续进行文件的解析操作，此处暂定同步进行
                    # 解析成功或者失败都应当基于前台提示框进行提示
                    # 注意，dialog 消失的时候是隐藏的，所以需要考虑 dialog 是否在每次操作后进行刷新处理

                # 上传组件
                upload = ui.upload(
                    label="选择文件",
                    on_upload=handle_upload,
                    multiple=False,  # 不支持多文件上传
                    max_file_size=max_file_size,
                    auto_upload=True  # 支持自动上传，这样似乎可以折中实现：只能上传一个文件
                ).classes("max-w-full").props(f'accept={",".join(accept)}')


if __name__ in {"__main__", "__mp_main__"}:
    dialog = UploadDialog()

    # 使用 ui.row().classes("w-full justify-center") 包裹按钮实现居中
    # 添加 mt-4 类提供上边距
    with ui.row().classes("w-full justify-center mt-4"):
        ui.button("文件上传",
                  icon="cloud_upload",  # 添加云上传图标
                  on_click=dialog.open,
                  color="primary")  # 设置主色调

    # UploadDialog()

    ui.run(host="localhost", port=10086, reload=False, show=False, favicon="🚀")
