import random
from typing import Optional

import requests
from loguru import logger

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


def account_tree_panel(panel, selected_menu):
    NODE_TYPE = {  # noqa: Variable in function should be lowercase
        '变电站': {'color': '#2196f3', 'symbol': 'circle'},
        '负载': {'color': '#4caf50', 'symbol': 'circle'},
        '发电机': {'color': '#ff9800', 'symbol': 'circle'},
    }

    # 生成50个节点，类型随机
    nodes = []
    for i in range(1, 51):
        if i % 10 == 0:
            t = '发电机'
            name = f'发电机{i // 10}'
        elif i % 7 == 0:
            t = '变电站'
            name = f'变电站{i // 7}'
        else:
            t = '负载'
            name = f'负载{i}'
        nodes.append({'id': i, 'name': name, 'type': t, 'power': f'{random.randint(50, 200)}MW'})

    # 随机生成边，保证连通性
    edges = []
    for i in range(2, 51):
        edges.append({'source': random.randint(1, i - 1), 'target': i})
    # 再加一些随机边
    for _ in range(30):
        s, t = random.sample(range(1, 51), 2)
        edges.append({'source': s, 'target': t})

    def get_topology_option(layout='force', node_size=15):
        # 生成 ECharts 配置
        return {
            'title': {'text': '33节点配电网拓扑结构', 'left': 'center', 'top': 20,
                      'textStyle': {'fontSize': 20}},
            'tooltip': {
                'trigger': 'item',
                'formatter': '''function(params){
                    if(params.dataType === 'node'){
                        return `<b>${params.data.name}</b><br>类型: ${params.data.type}<br>功率: ${params.data.power||'--'}<br>节点ID: ${params.data.id}`;
                    }
                    return '';
                }'''
            },
            'legend': [{
                'data': list(NODE_TYPE.keys()),
                'top': 40,
                'right': 40,
                'orient': 'vertical',
                'textStyle': {'fontSize': 14}
            }],
            'series': [{
                'type': 'graph',
                'layout': layout,
                'symbolSize': node_size,
                'roam': True,
                'label': {'show': True, 'position': 'right', 'fontSize': 12},
                'edgeSymbol': ['none', 'arrow'],
                'edgeSymbolSize': [4, 8],
                'data': [
                    {
                        'id': str(n['id']),
                        'name': n['name'],
                        'type': n['type'],
                        'category': n['type'],
                        'symbol': NODE_TYPE[n['type']]['symbol'],
                        'itemStyle': {'color': NODE_TYPE[n['type']]['color']},
                        'power': n.get('power', None)
                    }
                    for n in nodes
                ],
                'categories': [
                    {'name': k, 'itemStyle': {'color': v['color']}} for k, v in NODE_TYPE.items()
                ],
                'links': [
                    {'source': str(e['source']), 'target': str(e['target'])} for e in edges
                ],
                'lineStyle': {'color': '#aaa', 'width': 2},
                'emphasis': {'focus': 'adjacency', 'lineStyle': {'width': 4}},
            }]
        }

    selected_menu.text = "拓扑结构"
    with panel:
        # 控件区
        with ui.row().classes('items-center mb-4'):
            layout_type = ui.select(['力导向布局', '环形布局'], value='力导向布局', label='布局类型').classes(
                'w-40')
            ui.label('节点大小')
            node_size = ui.slider(min=10, max=30, value=15, step=1).classes('w-64 ml-4')
            refresh_btn = ui.button('刷新', icon='refresh').classes('ml-4')

        # 图表区
        chart = ui.echart(get_topology_option('force', 15)).classes(
            'w-full h-[600px] min-h-[400px] bg-white rounded shadow')

        # 交互逻辑
        def update_chart():
            layout = 'force' if layout_type.value == '力导向布局' else 'circular'
            chart.options = get_topology_option(layout, node_size.value)

        layout_type.on('update:model-value', lambda e: update_chart())
        node_size.on('update:model-value', lambda e: update_chart())
        refresh_btn.on('click', lambda: update_chart())


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


def assessment_panel(panel, selected_menu):
    dimensions = ['安全性', '可靠性', '经济性', '环保性', '灵活性']
    plans = [
        {'name': '方案一', 'scores': {'安全性': 90, '可靠性': 84, '经济性': 93, '环保性': 80, '灵活性': 76},
         'overall': 84.6, 'tags': ['绿色环保', '负载均衡']},
        {'name': '方案二', 'scores': {'安全性': 90, '可靠性': 78, '经济性': 80, '环保性': 92, '灵活性': 90},
         'overall': 85.0, 'tags': ['灵活性高', '负载均衡']},
        {'name': '方案三', 'scores': {'安全性': 76, '可靠性': 84, '经济性': 75, '环保性': 87, '灵活性': 86},
         'overall': 81.6, 'tags': ['综合优势', '灵活性高']}
    ]

    detail_data = {
        '安全性': {'线路负载率': [95, 80, 78], 'N-1通过率': [78, 85, 88], '电压越限率': [90, 90, 92],
                   '电压波动度': [86, 78, 85], '潮流不均衡度': [84, 77, 70]},
        '可靠性': {'供电可靠率': [90, 88, 85], '平均停电时间': [70, 75, 80], '重要负荷覆盖率': [85, 86, 88]},
        '经济性': {'购电成本': [82, 78, 76], '运行费用': [90, 85, 82], '发电成本': [89, 80, 75]},
        '环保性': {'碳排放量': [80, 70, 60], '污染物排放': [85, 77, 70], '可再生能源比重': [88, 92, 95]},
        '灵活性': {'可调负荷比例': [80, 85, 88], '备用容量': [75, 80, 85], '调节速度': [70, 82, 86]},
    }

    selected_menu.text = '多维度评估分析'

    with panel:
        # 顶部控件 + 雷达图
        with ui.row().classes('items-center justify-between'):
            ui.label('多维度综合评估').classes('text-lg font-bold')
            with ui.row().classes('items-center'):
                ui.select(['综合评估', '维度评估'], value='综合评估').classes('w-32')
                ui.select(['等权重', '专家权重'], value='等权重').classes('w-32 mx-2')
                ui.button('重新评估', icon='refresh').classes('bg-blue-500 text-white')

        ui.echart({
            'tooltip': {},
            'legend': {
                'data': [p['name'] for p in plans],
                'orient': 'vertical',
                'right': 10,
                'top': 'center'
            },
            'radar': {
                'indicator': [{'name': d, 'max': 100} for d in dimensions],
                'radius': '70%',  # 增加雷达图半径
                'center': ['50%', '50%']  # 确保居中
            },
            'series': [{
                'type': 'radar',
                'data': [
                    {'value': list(p['scores'].values()), 'name': p['name']} for p in plans
                ]
            }]
        }).classes('w-full h-[500px] my-4')

        # 下方：指标分析图
        with ui.tabs() as tabs:
            for dim in dimensions:
                ui.tab(dim)

        with ui.tab_panels(tabs=tabs, value=dimensions[0]).classes('w-full'):
            ui.label("指标分析图").classes('mb-2')
            for dim in dimensions:
                with ui.tab_panel(dim):
                    ui.label('详细指标分析').classes('font-bold mb-2')
                    subs = detail_data[dim]
                    ui.echart({
                        'tooltip': {},
                        'legend': {
                            'data': [p['name'] for p in plans],
                            'orient': 'vertical',
                            'right': 10,
                            'top': 'center'
                        },
                        'xAxis': {'type': 'category', 'data': list(subs.keys())},
                        'yAxis': {'type': 'value', 'max': 100},
                        'series': [
                            {
                                'type': 'bar',
                                'name': plans[i]['name'],
                                'data': [v[i] for v in subs.values()]
                            } for i in range(3)
                        ]
                    }).classes('w-full h-[500px] min-h-[300px]')


def solar_power_panel(panel, selected_menu):
    selected_menu.text = '光伏承载力分析'
    with panel:
        # 顶部选择控件
        with ui.row().classes('items-center justify-between mb-4'):
            ui.label('光伏发电承载力分析').classes('text-lg font-bold')
            with ui.row().classes('items-center'):
                ui.select(['晴天', '阴天', '多云'], value='晴天', label='天气条件').classes('w-32')
                ui.select(['春季', '夏季', '秋季', '冬季'], value='夏季', label='季节').classes('w-32 ml-2')
                ui.button('刷新数据', icon='refresh').classes('ml-2 bg-blue-500 text-white')

        # 发电量与消纳量曲线图
        hours = [f'{h}:00' for h in range(24)]
        gen = [round(random.uniform(0, 300) * max(0, 1 - abs(h - 12) / 12), 1) for h in range(24)]
        use = [round(g * random.uniform(0.8, 0.95), 1) for g in gen]
        ui.echart({
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['发电量', '消纳量']},
            'xAxis': {'type': 'category', 'data': hours},
            'yAxis': {'type': 'value', 'name': '功率(MW)'},
            'series': [
                {'name': '发电量', 'type': 'line', 'data': gen, 'areaStyle': {}},
                {'name': '消纳量', 'type': 'line', 'data': use, 'areaStyle': {}}
            ]
        }).classes('w-full h-96')

        # 总览指标卡片
        with ui.row().classes('w-full mt-6'):
            for label, value, icon, delta in [
                ('总装机容量', '850.5 MW', 'dns', 2.1),
                ('当前发电量', '625.3 MW', 'flash_on', 5.2),
                ('实际消纳量', '598.7 MW', 'power', 3.8),
                ('消纳效率', '95.7%', 'percent', 1.2)
            ]:
                with ui.card().classes('flex-1 text-center'):
                    ui.icon(icon).classes('text-yellow-500 text-2xl')
                    ui.label(label).classes('text-sm text-gray-500')
                    ui.label(value).classes('text-2xl font-bold my-1')
                    ui.label(f'+{delta:.1f}%').classes('text-green-500 text-xs')
                    ui.linear_progress(value=delta / 10).classes('mt-1')

        # 区域容量分布
        with ui.label('光伏容量区域分布').classes('text-base font-bold mt-8'):
            pass
        with ui.row().classes('w-full flex-wrap'):
            for name in ['区域A', '区域B', '区域C', '区域D', '区域E', '区域F']:
                cap = round(random.uniform(80, 150), 1)
                cur = round(cap * random.uniform(0.7, 0.95), 1)
                rate = round(cur / cap * 100, 1)
                status = '正常' if rate <= 90 else '高负载'
                tag_color = 'green' if rate <= 90 else 'red'
                with ui.card().classes('w-1/3 p-4 m-2'):
                    ui.label(name).classes('text-base font-bold')
                    ui.label(f'装机容量: {cap} MW').classes('text-sm')
                    ui.label(f'当前发电: {cur} MW').classes('text-sm')
                    ui.label(f'负载率: {rate}%').classes('text-sm')
                    ui.linear_progress(value=rate / 100, color='yellow').classes('mt-2')
                    ui.label(status).classes(f'text-xs text-{tag_color}-500')

        # 未来24小时预测图
        with ui.card().classes('w-full mt-6'):
            ui.label('未来24小时预测').classes('text-base font-bold mb-2')
            forecast = [round(700 * max(0, 1 - abs(h - 12) / 12) + random.uniform(-30, 30), 1) for h in range(24)]
            ui.echart({
                'tooltip': {'trigger': 'axis'},
                'xAxis': {'type': 'category', 'data': hours},
                'yAxis': {'type': 'value', 'name': '功率(kW)'},
                'series': [{
                    'type': 'line',
                    'name': '发电预测',
                    'data': forecast,
                    'areaStyle': {'color': '#ffe58f'}
                }]
            }).classes('w-full h-80')
        return


# 菜单项
menu_items = [
    {'name': '系统概览', 'icon': 'dashboard', "fn": dashboard_panel},
    {'name': '拓扑结构', 'icon': 'account_tree', "fn": account_tree_panel},
    {'name': '潮流计算', 'icon': 'calculate', "fn": calculate_panel},
    {'name': '光伏承载力', 'icon': 'solar_power', "fn": solar_power_panel},
    {'name': '多维度评估', 'icon': 'assessment', "fn": assessment_panel},
]


# todo: 好好深入 nicegui
# todo: 多阅读框架源代码，多学习吸收优秀的代码
# todo: 确定 ui.page 和不设置的区别 | 全局变量不同页面是否独立 | 页面间数据传递 | ui.page 做了什么，请深入 vue ...
@ui.page("/")
async def main():
    # 创建主布局
    with ui.row().classes('w-full h-screen'):
        # 左侧导航菜单 (1/7宽度)
        with ui.column().classes('flex-[1] bg-blue-50 h-full p-4 shadow-md'):
            # 菜单标题
            with ui.column().classes('mb-4'):
                with ui.row().classes('items-center'):
                    ui.icon('bolt').classes('text-yellow-500 text-2xl mr-2')
                    ui.label('柔性配电评估系统').classes('text-xl font-bold text-blue-800')
                ui.label('多维度评估与可视化平台').classes('text-xs text-blue-600 mt-1 ml-8')

            # 创建菜单项并添加点击效果
            for item in menu_items:
                def get_on_click(_item):
                    return lambda: select_menu(_item)

                with ui.button(on_click=get_on_click(item)) \
                        .classes('w-full justify-start mb-2 text-blue-900') \
                        .props(f'flat icon={item["icon"]}'):
                    ui.label(item['name']).classes('ml-2')

        # 右侧自定义面板 (6/7宽度)
        with ui.column().classes('flex-[6] h-full p-8'):
            # 标题区域
            selected_menu = ui.label('自定义内容面板').classes('text-2xl font-bold mb-6 text-blue-700')

            # 自定义面板容器 (留出空间供用户自定义)
            custom_panel = ui.column().classes(
                'w-full h-11/12 bg-white rounded-lg shadow-lg p-4 border border-blue-100')
            custom_panel.style('overflow-y: auto;')

            # 初始占位内容
            with custom_panel:
                ui.label('请从左侧菜单选择功能').classes('text-gray-500 text-xl mt-10 text-center')
                ui.icon('arrow_back').classes('text-4xl text-gray-400 mx-auto mt-4')
                ui.label('此区域可用于展示电力系统数据、图表和计算结果').classes('text-center text-gray-600 mt-8')

    async def select_menu(item):
        # await pre_check_and_redirect()
        selected_menu.text = f'{item["name"]} 功能面板'
        custom_panel.clear()

        if item["fn"]:
            item["fn"](custom_panel, selected_menu)
            return

    # todo: 弄明白 python async 不同调用方式的区别，为什么 ide 无法智能提示？
    async def pre_check_and_redirect():
        try:
            # fixme: 此处无效，不太对，可恶，nicegui 感觉实现稍微复杂一点的内容，在不知道背后原理的情况下，很难...
            #        感觉必须要了解 nicegui 的实现原理，才能灵活运用！必须深入了解一下它的原理啊！
            # todo: 此处不允许使用 requests，请使用 aiohttp
            logger.info("123")
            url = "http://127.0.0.1:8888/index/heart_beat/verify_identity/"
            resp = requests.get(url, timeout=3)
            if resp.url != url:
                # 如果是 HTTP 重定向
                # redirect_url = resp.headers.get('Location', '/')
                redirect_url = "http://127.0.0.1:8888/"
                logger.debug(redirect_url)
                await ui.run_javascript(f"window.open('{redirect_url}', '_blank')")
                return True
            elif resp.ok:
                data = resp.json()
                if data.get('redirect'):
                    await ui.run_javascript(f"window.open('{data['redirect']}', '_blank')")
                    return True
        except Exception as e:
            logger.error('行号：{}，预检查失败：{}', "unknown", e)
        return False

    # todo: 页面加载完的一瞬间，立刻发出一个权限探测请求，用于检测用户权限，并返回结果
    # [answer] 这个有待深入，目前不知道该如何实现，但是显然刷新的时候肯定会调用后端请求来获取数据，
    #          那么我认为后端不应该重定向，而是返回指定响应，由前端重定向！

    # todo: 了解 Tailwind CSS 类，比如：w-full: 宽度为父容器的 100%，h-11/12: 高度为父容器的 11/12 (约 91.67%)

    # [note] 收获：ai 编程 + nicegui 可以很快做出不错的静态页面，但是微调有点复杂，可能前端就是如此？

    # 测试发现，select_menu 为什么会一直被执行？nicegui 不知道原理的话实在有些痛苦
    await select_menu(menu_items[0])


if __name__ == '__main__':
    # 实际上启动了 FastAPI 服务器
    ui.run(title="柔性配电评估系统", host="localhost", port=12000, reload=False, show=False, favicon="🚀")
