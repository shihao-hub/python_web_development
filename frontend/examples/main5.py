import base64
import tempfile
import time
import datetime
from io import BytesIO
from functools import cache
from pathlib import Path
from typing import Set

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger

from nicegui import ui

tempfilenames: Set[str] = set()


@cache
def save_base64_image(base64_str: str) -> Path:
    """将 Base64 编码的图片数据解码并保存到临时文件中"""

    now_stamp = time.time()
    file_name = f"./{now_stamp}.png"

    try:
        # 解码 Base64 字符串
        image_data = base64.b64decode(base64_str)
    except Exception as e:
        raise ValueError("无效的 Base64 数据") from e

    # todo: 检测图片类型
    file_extension = "png"

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
        temp_file.write(image_data)
        temp_path = Path(temp_file.name)

    logger.info("图片已保存到临时文件: {}", temp_path)
    tempfilenames.add(str(temp_path))
    return temp_path


def update_plot(e):
    frequency = frequency_knob.value
    amplitude = amplitude_knob.value

    # 生成波形
    x = np.linspace(0, 2 * np.pi, 100)
    y = amplitude * np.sin(frequency * x)

    # 更新图表
    plt.figure(figsize=(4, 2))
    plt.plot(x, y, 'b-')
    plt.ylim(-5, 5)
    plt.tight_layout()

    # 转换为base64图像
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode()

    # todo: 修改为异步操作
    img_path = save_base64_image(img_data)

    with image_carousel_panel:
        logger.debug("image_carousel_panel: {}", image_carousel_panel)
        ui.image(str(img_path))
    # 使用完成后删除临时文件（可选）
    # tempfilenames.remove(str(img_path))
    # img_path.unlink()

    plot.src = f'data:image/png;base64,{img_data}'
    plot.update()
    plt.close()


# 创建控制面板
with ui.row().classes('w-full justify-center'):
    with ui.card().classes('w-48 items-center'):
        frequency_knob = ui.knob(2, min=0.1, max=5, step=0.1,
                                 color='#8b5cf6')
        amplitude_knob = ui.knob(3, min=0.5, max=5, step=0.1,
                                 color='#ec4899')

        # 绑定更新事件
        frequency_knob.on('update:model-value', lambda e: (
            # logger.debug("frequency_knob on update:model-value"),
            update_plot(e),
        ))
        amplitude_knob.on('update:model-value', update_plot)

    # 创建图片轮播面板
    with ui.card().classes('w-96 items-center').style("border: 1px solid #000;"):
        with ui.carousel().classes('w-full') as image_carousel_panel:
            pass

# 初始图表
plot = ui.image().classes('w-full').style("border: 1px solid #ccc;")

# ui.run()

# todo: 有无程序崩溃回调？

ui.run(host="localhost", port=14001, reload=False, show=False, favicon="🚀")
