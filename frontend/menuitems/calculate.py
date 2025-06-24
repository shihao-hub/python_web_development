import random

from nicegui import ui


def calculate_panel(panel, selected_menu):
    selected_menu.text = '电网潮流计算'
    with panel:
        # 顶部：标题 + 控件区
        with ui.row().classes('items-center justify-between mb-4'):
            ui.label('电网潮流分布').classes('text-lg font-bold')
            with ui.row().classes('items-center'):
                ui.select(['牛顿-拉夫逊法', '直流潮流法', '快速潮流法'], value='牛顿-拉夫逊法').classes('w-40')
                ui.label('收敛精度').classes('ml-2')
                ui.slider(min=0.001, max=0.01, value=0.001, step=0.001).classes('w-32')
                ui.button('开始计算', icon='play_arrow').classes('ml-2 bg-blue-500 text-white')
                ui.button('刷新数据', icon='refresh').classes('ml-2')

        # 随机生成潮流数据
        hours = [f'{h}:00' for h in range(24)]
        active_power = [round(random.uniform(600, 1000) + (50 if 6 <= h <= 18 else 0), 2) for h in range(24)]
        reactive_power = [round(p * random.uniform(0.25, 0.35), 2) for p in active_power]
        voltage = [round(random.uniform(100, 250), 1) for _ in range(24)]

        # 折线图
        ui.echart({
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['有功功率', '无功功率', '电压']},
            'xAxis': {'type': 'category', 'data': hours},
            'yAxis': [
                {'type': 'value', 'name': '功率 (MW)'},
                {'type': 'value', 'name': '电压 (V)', 'position': 'right'}
            ],
            'series': [
                {'name': '有功功率', 'type': 'line', 'data': active_power, 'areaStyle': {}},
                {'name': '无功功率', 'type': 'line', 'data': reactive_power, 'areaStyle': {}},
                {'name': '电压', 'type': 'line', 'data': voltage, 'yAxisIndex': 1, 'areaStyle': {}}
            ]
        }).classes('w-full h-96')

        # 实时监控指标卡片
        total_power = round(sum(active_power) / len(active_power), 2)
        max_load = round(random.uniform(85, 95), 2)
        voltage_deviation = round(random.uniform(1.8, 3.0), 2)
        network_loss = round(random.uniform(3.5, 5.0), 2)
        delta_color = lambda v: 'text-green-500' if v >= 0 else 'text-red-500'
        with ui.row().classes('w-full mt-6'):
            for label, value, delta in [
                ('总功率', f'{total_power} MW', round(random.uniform(-2, 2), 2)),
                ('最大负载率', f'{max_load}%', round(random.uniform(-2, 2), 2)),
                ('电压偏差', f'{voltage_deviation}%', round(random.uniform(-1, 1), 2)),
                ('网损率', f'{network_loss}%', round(random.uniform(-1, 1), 2))
            ]:
                with ui.card().classes('flex-1 text-center'):
                    ui.label(label).classes('text-sm text-gray-500')
                    ui.label(value).classes('text-2xl font-bold my-1')
                    ui.label(f"{('+' if delta >= 0 else '')}{delta:.2f}%").classes(
                        f'text-xs {delta_color(delta)}')

        # 线路负载列表
        with ui.card().classes('w-full mt-6'):
            ui.label('线路负载详情').classes('text-base font-bold mb-4')
            with ui.column():
                for i in range(1, 6):
                    load = round(random.uniform(60, 95), 1)
                    power = round(random.uniform(10, 15), 2)
                    current = round(random.uniform(90, 140), 1)
                    with ui.row().classes('items-center justify-between py-2 border-b'):
                        ui.label(f'线路{i}-{i + 1} 节点{i} → 节点{i + 1}')
                        ui.label(f'负载率: {load}%')
                        ui.label(f'功率: {power} MW')
                        ui.label(f'电流: {current} A')
                        ui.linear_progress(value=load / 100).classes('w-32')
