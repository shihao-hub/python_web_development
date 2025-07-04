import os
from typing import Optional

import plotly.graph_objects as go
from nicegui import ui

fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[1, 2, 3, 2.5]))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
ui.plotly(fig).classes('w-full h-40')

# ui.plotly: https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/data/plotly.html
# todo: plotly 第三方库
# todo: 明确一下，这些图有些不好理解，数据分析里也是这样的，感觉这些库应该都是科学家写的一样或者数学家？或者单纯不熟悉？
# [note] 并没有好好研究，用到再学才行

ui.run(host="localhost", port=14000, reload=False, show=False, favicon="🚀", storage_secret="123")
