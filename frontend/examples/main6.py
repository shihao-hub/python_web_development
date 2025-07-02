from nicegui import ui
import base64
import tempfile
import os
from pathlib import Path
from typing import List


class ImageCarousel:
    def __init__(self, images: List[str], title: str = "图片轮播"):
        """
        图片轮播组件

        参数:
            images: 图片列表 (可以是URL、本地路径或Base64编码的图片)
            title: 轮播图标题
        """
        self.images = images
        self.current_index = 0
        self.title = title
        self.temp_files = []  # 用于存储临时文件路径

        # 创建轮播UI
        self._create_carousel()

        # 自动清理临时文件
        # ui.timer(5.0, self.cleanup_temp_files, once=True)

    def _create_carousel(self):
        """创建轮播组件"""
        with ui.card().classes("w-full max-w-2xl mx-auto shadow-lg rounded-xl overflow-hidden"):
            # 标题栏
            with ui.row().classes("w-full bg-blue-500 text-white p-4 items-center justify-between"):
                ui.label(self.title).classes("text-xl font-bold")
                ui.label().bind_text_from(self, "position_info")

            ui.image(r"C:\Users\z30072623\AppData\Local\Temp\tmpsjee4rmb.png")

            # 轮播图区域
            with ui.column().classes("relative w-full h-80 overflow-hidden"):
                self.carousel = ui.carousel(animated=True, arrows=False).classes("w-full h-full")
                with self.carousel:
                    for idx, img_data in enumerate(self.images):
                        # 处理不同类型的图片数据
                        if img_data.startswith('http'):
                            # 网络图片
                            ui.image(img_data).classes("w-full h-full object-contain")
                        elif os.path.exists(img_data):
                            # 本地图片
                            ui.image(img_data).classes("w-full h-full object-contain")
                        else:
                            # Base64图片
                            temp_path = self.save_base64_image(img_data)
                            ui.image(str(temp_path)).classes("w-full h-full object-contain")

                # 叠加层显示当前图片信息
                with ui.column().classes("absolute bottom-0 left-0 w-full bg-black bg-opacity-50 text-white p-2"):
                    ui.label().bind_text_from(self, "current_info")

            # 控制按钮区域
            with ui.row().classes("w-full p-4 bg-gray-100 justify-center items-center gap-4"):
                ui.button(icon="chevron_left", on_click=self.prev_image) \
                    .props("round dense").classes("bg-blue-500 text-white")

                # 缩略图预览
                with ui.row().classes("flex-1 justify-center overflow-x-auto gap-2 py-2 no-wrap"):
                    for idx in range(len(self.images)):
                        ui.button("", on_click=lambda idx=idx: self.goto_image(idx)) \
                            .props("round dense") \
                            .classes(f"w-8 h-8 min-w-8 {self.get_thumb_class(idx)}") \
                            # .bind_text(str(idx + 1))

                ui.button(icon="chevron_right", on_click=self.next_image) \
                    .props("round dense").classes("bg-blue-500 text-white")

    @property
    def position_info(self):
        """当前位置信息"""
        return f"{self.current_index + 1}/{len(self.images)}"

    @property
    def current_info(self):
        """当前图片信息"""
        return f"图片 {self.current_index + 1} - 共 {len(self.images)} 张"

    def get_thumb_class(self, idx: int) -> str:
        """获取缩略图按钮的样式类"""
        return "bg-blue-500 text-white" if idx == self.current_index else "bg-gray-300"

    def goto_image(self, index: int):
        """跳转到指定图片"""
        self.current_index = index
        self.carousel.value = index
        self.carousel.update()

    def next_image(self):
        """下一张图片"""
        self.current_index = (self.current_index + 1) % len(self.images)
        self.carousel.next()

    def prev_image(self):
        """上一张图片"""
        self.current_index = (self.current_index - 1) % len(self.images)
        self.carousel.prev()

    def save_base64_image(self, base64_str: str) -> Path:
        """保存Base64图片到临时文件"""
        # 移除可能的Data URI前缀
        if base64_str.startswith('data:'):
            base64_str = base64_str.split(',', 1)[1]

        # 解码Base64
        image_data = base64.b64decode(base64_str)

        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_file.write(image_data)
            temp_path = Path(temp_file.name)

        # 存储临时文件路径以便后续清理
        self.temp_files.append(temp_path)
        return temp_path

    def cleanup_temp_files(self):
        """清理临时文件"""
        for path in self.temp_files:
            try:
                if path.exists():
                    path.unlink()
            except Exception as e:
                ui.notify(f"删除临时文件失败: {str(e)}", type="warning")
        self.temp_files.clear()


# 示例图片数据
# 可以是URL、本地路径或Base64编码的图片
image_sources = [
    # Base64示例图片 (1x1红色像素)
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",

    # 网络图片URL
    "https://picsum.photos/800/600?random=1",

    # 本地图片路径 (需要替换为实际存在的图片)
    # "path/to/local/image.jpg",

    # 另一个Base64示例 (1x1蓝色像素)
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",

    # 另一个网络图片
    "https://picsum.photos/800/600?random=2",

    # 再一个Base64示例 (1x1绿色像素)
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",

    r"C:\Users\z30072623\AppData\Local\Temp\tmpsjee4rmb.png",
]

# 创建轮播组件
carousel = ImageCarousel(
    images=image_sources,
    title="我的图片收藏集"
)

# 添加说明
with ui.card().classes("w-full max-w-2xl mx-auto mt-8 p-4 bg-blue-50"):
    ui.label("使用说明").classes("text-lg font-bold text-blue-800")
    with ui.list().classes("list-disc pl-6 text-blue-700"):
        ui.item("点击左右箭头按钮切换图片")
        ui.item("点击底部的数字按钮可跳转到指定图片")
        ui.item("当前图片位置显示在顶部右侧")
        ui.item("当前图片信息显示在图片底部")
        ui.item("Base64图片会自动保存为临时文件并显示")

# 添加自定义图片上传功能
with ui.card().classes("w-full max-w-2xl mx-auto mt-8 p-4 bg-green-50"):
    ui.label("添加自定义图片").classes("text-lg font-bold text-green-800")


    def handle_upload(e):
        """处理图片上传"""
        if e.type == "data_url":
            # 添加Base64图片到轮播
            image_sources.append(e.content)
            carousel.images = image_sources
            ui.notify(f"成功添加新图片! 当前共 {len(image_sources)} 张图片")


    ui.upload(
        label="上传图片",
        on_upload=handle_upload,
        max_file_size=3_000_000,  # 3MB
        max_files=5,
        auto_upload=True
    ).props('accept=".jpg,.jpeg,.png,.gif" multiple')

# 添加主题切换
dark_mode = ui.dark_mode()
ui.button("切换主题", icon="dark_mode", on_click=dark_mode.toggle).classes("fixed bottom-4 right-4")

# 启动应用
ui.run(host="localhost", port=14002, reload=False, show=False, favicon="🚀")
