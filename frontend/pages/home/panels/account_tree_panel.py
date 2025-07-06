import random

from loguru import logger

from nicegui import ui

from frontend.services import fetch_topology_data


def account_tree_panel0(panel, selected_menu):
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


def account_tree_panel(panel, selected_menu):
    logger.debug("call account_tree_panel")
    data = fetch_topology_data()
    logger.debug("data: {}", data)
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])

    NODE_TYPE = {
        '变电站': {'symbol': 'rect', 'color': '#3478f6'},
        '负载': {'symbol': 'circle', 'color': '#44b07b'},
        '发电机': {'symbol': 'diamond', 'color': '#f68b2c'},
    }

    def get_topology_option(layout='force', node_size=30):
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
