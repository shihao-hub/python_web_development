import math
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plt
from loguru import logger

from nicegui import ui

line_plot = ui.line_plot(n=2, limit=20, figsize=(3, 2), update_every=5) \
    .with_legend(['sin', 'cos'], loc='upper center', ncol=2)

# todo: 确实旋转了，但是也被遮挡了呀...
# plt.xticks(rotation=90)

last_time: Optional[float] = None


def update_line_plot() -> None:
    global last_time
    if last_time is None:
        last_time = datetime.now().timestamp()
    now = datetime.now()
    x = now.timestamp()
    logger.debug("x: {} type: {}, interval: {}", x, type(x), x - last_time)
    last_time = x
    y1 = math.sin(x)
    y2 = math.cos(x)
    # todo: to understood the first parameter of line_plot.push()
    line_plot.push([x], [[y1], [y2]])


line_updates = ui.timer(0.1, update_line_plot, active=False)
line_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
