import asyncio
import pprint
import random
from typing import Dict, List, Tuple
from datetime import datetime

from loguru import logger

from nicegui import ui

# 1. 仪表板布局和样式设置
ui.add_head_html('''
<style>
    body {
        background: linear-gradient(135deg, #1a2a6c, #2a4d69, #4b86b4);
        color: #fff;
        min-height: 100vh;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .custom-select {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        padding: 14px 18px !important;
        border-radius: 10px !important;
    }

    .custom-select:hover {
        border-color: #ff7e5f !important;
    }

    .spinner {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(255, 255, 255, 0.2);
        border-top: 5px solid #ff7e5f;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 20px;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
''')


# 2. 模拟数据
class DataService:
    def __init__(self):
        self.mock_data = {
            'sales': {
                'weekly': [120, 190, 140, 180, 160, 150, 200],
                'monthly': [420, 530, 480, 560, 610, 580, 650, 720, 680, 710, 740, 690],
                'quarterly': [1250, 1380, 1420, 1560],
                'yearly': [4800, 5200, 6100, 6900, 7500, 8200]
            },
            'revenue': {
                'weekly': [85, 110, 95, 120, 105, 130, 145],
                'monthly': [320, 410, 380, 450, 490, 520, 580, 620, 590, 630, 670, 710],
                'quarterly': [980, 1150, 1220, 1380],
                'yearly': [4200, 4800, 5500, 6200, 6900, 7600]
            },
            'users': {
                'weekly': [350, 420, 380, 410, 460, 480, 520],
                'monthly': [1250, 1380, 1420, 1560, 1680, 1750, 1820, 1920, 2010, 2150, 2240, 2380],
                'quarterly': [4800, 5200, 5800, 6400],
                'yearly': [18500, 21500, 24500, 27800, 31200, 34500]
            },
            'traffic': {
                'weekly': [12500, 14200, 13800, 15600, 16200, 17500, 18400],
                'monthly': [48500, 52000, 53800, 56200, 59800, 61500, 64200, 68500, 69800, 72400, 75800, 78200],
                'quarterly': [158000, 168000, 182000, 195000],
                'yearly': [685000, 725000, 798000, 845000, 925000, 1025000]
            }
        }

    def get_data(self, category: str, time_range: str) -> Tuple[List[str], List[float]]:
        labels = self.generate_labels(time_range)
        data = self.mock_data[category][time_range]
        return labels, data

    def generate_labels(self, time_range: str) -> List[str]:
        if time_range == 'weekly':
            return ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        elif time_range == 'monthly':
            return [f'{i + 1}月' for i in range(12)]
        elif time_range == 'quarterly':
            return ['第一季度', '第二季度', '第三季度', '第四季度']
        elif time_range == 'yearly':
            return ['2018', '2019', '2020', '2021', '2022', '2023']
        return []


# 3. 创建仪表板组件
class Dashboard:
    def __init__(self):
        self.data_service = DataService()
        self.loading = False
        self.last_updated = "刚刚"

        self._construct_skeleton_and_skin()

    def _construct_skeleton_and_skin(self):
        # 创建 UI
        # 命名以 _ 开头的目的是：只有这样 self.x = y 才不会被 ide 警告。
        # 最初编写的时候，推荐这个页面就写在这一个方法里，后续再提取出去
        self._create_header()
        self._create_control_panel()
        self._create_chart_panel()  # noqa: {0} is not callable
        self._create_footer()

    def _create_header(self):
        with ui.header().classes('text-center py-8 mb-8'):
            ui.label('动态数据可视化仪表板').classes(
                'text-4xl md:text-5xl font-bold mb-4 '
                'bg-gradient-to-r from-orange-400 to-orange-300 '
                'bg-clip-text text-transparent '
                'drop-shadow-lg'
            )
            ui.label('使用下拉菜单选择不同数据集，实时查看图表动态变化效果').classes(
                'text-lg md:text-xl text-gray-300/80 '
                'max-w-2xl mx-auto leading-relaxed'
            )

    def _create_control_panel(self):
        with ui.column().classes('glass-panel p-6 mb-8 w-full'):
            with ui.row().classes('items-center mb-6'):
                ui.icon('insert_chart').classes(
                    'text-3xl bg-gradient-to-r from-orange-400 to-orange-300 '
                    'p-3 rounded-lg text-white'
                )
                ui.label('数据控制面板').classes('text-2xl ml-3')

            with ui.row().classes('w-full gap-4'):
                with ui.column().classes('min-w-[250px] flex-1'):
                    ui.label('选择数据类别：').classes('text-lg mb-2')
                    self.category_select = ui.select(
                        options={
                            'sales': '销售数据',
                            'revenue': '营收数据',
                            'users': '用户数据',
                            'traffic': '流量数据'
                        },
                        value='sales'
                    ).classes('custom-select w-full').on('update:model-value', self.update_chart)

                with ui.column().classes('min-w-[250px] flex-1'):
                    ui.label('选择时间范围：').classes('text-lg mb-2')
                    self.time_range_select = ui.select(
                        options={
                            'weekly': '本周数据',
                            'monthly': '本月数据',
                            'quarterly': '本季度数据',
                            'yearly': '年度数据'
                        },
                        value='monthly'
                    ).classes('custom-select w-full').on('update:model-value', self.update_chart)

    @ui.refreshable
    def _create_chart_panel(self):
        logger.info("call _create_chart_panel")
        with ui.column().classes('glass-panel p-6 w-full h-[500px]'):
            with ui.row().classes('w-full justify-between items-center mb-6'):
                ui.label('数据趋势图表').classes('text-2xl')
                self.last_updated_label = ui.label(f'最后更新: {self.last_updated}')

            self.chart = ui.echart({
                'title': {
                    'text': '数据趋势',
                    'textStyle': {
                        'color': '#fff'
                    }
                },
                'tooltip': {
                    'trigger': 'axis'
                },
                'legend': {
                    'data': [],
                    'textStyle': {
                        'color': 'rgba(255, 255, 255, 0.7)'
                    }
                },
                'grid': {
                    'left': '3%',
                    'right': '4%',
                    'bottom': '3%',
                    'containLabel': True
                },
                'xAxis': {
                    'type': 'category',
                    'boundaryGap': False,
                    'data': [],
                    'axisLabel': {
                        'color': 'rgba(255, 255, 255, 0.7)'
                    },
                    'axisLine': {
                        'lineStyle': {
                            'color': 'rgba(255, 255, 255, 0.2)'
                        }
                    }
                },
                'yAxis': {
                    'type': 'value',
                    'axisLabel': {
                        'color': 'rgba(255, 255, 255, 0.7)'
                    },
                    'axisLine': {
                        'show': False
                    },
                    'splitLine': {
                        'lineStyle': {
                            'color': 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                },
                'series': [{
                    'name': '',
                    'type': 'line',
                    'data': [],
                    'symbol': 'circle',
                    'symbolSize': 8,
                    'lineStyle': {
                        'width': 3,
                        'color': '#ff7e5f'
                    },
                    'itemStyle': {
                        'color': '#ff7e5f',
                        'borderColor': '#fff',
                        'borderWidth': 2
                    },
                    'areaStyle': {
                        'color': {
                            'type': 'linear',
                            'x': 0,
                            'y': 0,
                            'x2': 0,
                            'y2': 1,
                            'colorStops': [{
                                'offset': 0,
                                'color': 'rgba(255, 126, 95, 0.3)'
                            }, {
                                'offset': 1,
                                'color': 'rgba(255, 126, 95, 0)'
                            }]
                        }
                    }}]
            }).classes('w-full h-full')

            # 加载状态
            self.loading_overlay = ui.column().classes(
                'absolute inset-0 bg-black/70 items-center justify-center'
            ).style('display: none; z-index: 10;')
            with self.loading_overlay:
                ui.element('div').classes('spinner')
                ui.label('正在加载数据...')

            # todo: 加载完毕后，选择一下下拉框，触发更新操作？

    def _create_footer(self):
        with ui.footer().classes('text-center mt-8 opacity-70'):
            ui.label('© 2023 数据可视化仪表板 | 使用NiceGUI实现')

    async def update_chart(self):
        # [note] 通过 self.x 的方式，让我不需要通过 getElementByID 的方式去定位元素

        logger.info("call update_chart")
        self.show_loading()

        # 模拟API延迟
        await asyncio.sleep(0.8)

        # todo: 牢记类的优点，这些东西果然还是要多写项目，看运气说不一定就刷到题了一样的感觉...
        #       注意，推荐让 ai 用面向对象的思想编写 nicegui 代码，最好还能有 MVC 架构
        category = self.category_select.value
        time_range = self.time_range_select.value

        labels, data = self.data_service.get_data(category, time_range)

        # 更新图表
        self.chart.options['xAxis']['data'] = labels
        self.chart.options['series'][0]['data'] = data
        self.chart.options['series'][0]['name'] = self.get_chart_title(category, time_range)
        self.chart.update()

        # 更新最后更新时间
        self.update_timestamp()
        self.hide_loading()

        # 这个似乎不需要
        # self._create_chart_panel.refresh()

    def get_chart_title(self, category: str, time_range: str) -> str:
        category_map = {
            'sales': '销售额',
            'revenue': '营收额',
            'users': '用户数',
            'traffic': '访问量'
        }

        time_map = {
            'weekly': '本周',
            'monthly': '本月',
            'quarterly': '本季度',
            'yearly': '年度'
        }

        return f"{time_map[time_range]}{category_map[category]}"

    def update_timestamp(self):
        now = datetime.now().strftime('%H:%M')
        self.last_updated = now
        self.last_updated_label.text = f'最后更新: {now}'

    def show_loading(self):
        self.loading = True
        self.loading_overlay.style('display: flex;')

    def hide_loading(self):
        self.loading = False
        self.loading_overlay.style('display: none;')


# 4. 运行仪表板
if __name__ in {"__main__", "__mp_main__"}:
    dashboard = Dashboard()
    ui.run(title="动态数据可视化仪表板", host="localhost", port=13000, reload=False, show=False, dark=True, favicon="🚀")
