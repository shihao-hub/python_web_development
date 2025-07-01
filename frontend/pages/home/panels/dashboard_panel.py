import random
from typing import Optional

from nicegui import ui
from nicegui.element import Element


def dashboard_panel(panel, selected_menu):
    selected_time_range = '今日'
    selected_freq = '15分钟'

    top_statistic_cards: Optional[Element] = None

    def refresh_top_statistic_cards():
        top_statistic_cards.clear()

        cards = [
            {'title': '安全性', 'value': 93.8, 'icon': 'security', 'color': 'red', 'desc': '较昨日↑10.8%'},
            {'title': '经济性', 'value': 91.7, 'icon': 'paid', 'color': 'green', 'desc': '较昨日↑10.2%'},
            {'title': '可靠性', 'value': 100, 'icon': 'bolt', 'color': 'blue', 'desc': '较昨日↑10.8%'},
            {'title': '环保性', 'value': 91.2, 'icon': 'eco', 'color': 'lime', 'desc': '较昨日↑10.9%'},
        ]

        # 临时添加个 tag 用于标识变化
        # [note] global selected_time_range 和 selected_freq 可以这样用，大概率是因为这里就是 js 的天生单线程
        for c in cards:
            c["title"] = f"{c["title"]} - {selected_time_range} - {selected_freq}"

        with top_statistic_cards:
            for c in cards:
                with ui.card().classes('flex-1 mx-2'):
                    ui.icon(c['icon']).classes(f'text-3xl text-{c["color"]}-500')
                    ui.label(f'{c["value"]}').classes('text-2xl font-bold')
                    ui.label(c['title']).classes('text-base text-gray-600')
                    ui.linear_progress(value=c['value'] / 100, color=c['color']).classes('my-2')
                    ui.label(c['desc']).classes('text-xs text-gray-400')

    def refresh_dashboard():
        # doc: 整体刷新，简单方便，出现性能问题再说！
        # 这里写刷新逻辑，比如刷新统计卡片、图表等
        refresh_top_statistic_cards()
        # 你可以根据 selected_time_range 和 selected_freq 重新生成数据

    def on_time_range_change(value):
        nonlocal selected_time_range
        selected_time_range = value
        refresh_dashboard()

    def on_freq_change(value):
        nonlocal selected_freq
        selected_freq = value
        refresh_dashboard()

    selected_menu.text = "系统概览"
    with panel:
        with ui.row().classes('w-full items-center justify-between mb-4'):
            # 左侧标题和副标题
            with ui.column().classes(''):
                ui.label('柔性配电网络多维度评估系统').classes('text-xl font-bold text-gray-800')
                ui.label('动态承载力分析 · 多维度评估 · 实时监控').classes('text-xs text-gray-500 mt-1')

            # 右侧筛选和按钮
            with ui.row().classes('items-center'):
                ui.label('时间范围').classes('text-sm text-gray-600 mr-1')
                ui.select(['今日', '本周', '本月'], value=selected_time_range,
                          on_change=lambda e: on_time_range_change(e.value)).classes('mr-4 w-24')
                ui.label('数据频率').classes('text-sm text-gray-600 mr-1')
                ui.select(['15分钟', '1小时', '1天'], value=selected_freq,
                          on_change=lambda e: on_freq_change(e.value)).classes('mr-4 w-24')
                ui.button('刷新数据', icon='refresh', on_click=refresh_dashboard).classes('bg-blue-500 text-white')

        # 顶部四个统计卡片
        top_statistic_cards = ui.row().classes('w-full mb-6')
        refresh_top_statistic_cards()

        # 中间：左-折线图，右-雷达图
        with ui.row().classes('w-full mb-6'):
            # 折线图
            with ui.card().classes('flex-[3] mr-4'):
                ui.label('光伏发电承载力分析').classes('font-bold mb-2')
                hours = [f'{h}:00' for h in range(0, 24, 2)]
                gen = [random.randint(0, 300) if 6 <= h <= 18 else 0 for h in range(0, 24, 2)]
                load = [g - random.randint(0, 40) for g in gen]
                ui.echart({
                    'xAxis': {'type': 'category', 'data': hours},
                    'yAxis': {'type': 'value', 'name': '功率(MW)'},
                    'series': [
                        {'name': '发电量', 'type': 'line', 'data': gen, 'smooth': True, 'areaStyle': {}},
                        {'name': '消纳量', 'type': 'line', 'data': load, 'smooth': True, 'areaStyle': {}},
                    ],
                    'legend': {'data': ['发电量', '消纳量']},
                    'tooltip': {},
                }).classes('w-full h-64')

            # 雷达图
            with ui.card().classes('flex-[2]'):
                ui.label('多维度评估指标').classes('font-bold mb-2')
                radar_labels = ['安全性', '经济性', '可靠性', '灵活性', '环保性']
                current = [random.randint(80, 100) for _ in radar_labels]
                compare = [v - random.randint(0, 10) for v in current]
                ui.echart({
                    'radar': {
                        'indicator': [{'name': l, 'max': 100} for l in radar_labels],
                    },
                    'series': [{
                        'type': 'radar',
                        'data': [
                            {'value': current, 'name': '当前系统'},
                            {'value': compare, 'name': '对比方案'},
                        ]
                    }],
                    'legend': {
                        'data': ['当前系统', '对比方案'],
                        'orient': 'vertical',
                        'right': 10,
                        'top': 'center'
                    },
                }).classes('w-full h-64')

        # 下方：条形图
        with ui.card().classes('w-full'):
            ui.label('详细指标得分').classes('font-bold mb-2')
            bar_labels = ['潮流不均衡度', '电压波动度', '电压越限率', 'N-1通过率', '线路负载率']
            bar_values = [random.randint(60, 100) for _ in bar_labels]
            ui.echart({
                'xAxis': {'type': 'value', 'max': 100},
                'yAxis': {'type': 'category', 'data': bar_labels},
                'series': [{
                    'type': 'bar',
                    'data': bar_values,
                    'label': {'show': True, 'position': 'right'}
                }],
                'tooltip': {},
            }).classes('w-full h-64')
