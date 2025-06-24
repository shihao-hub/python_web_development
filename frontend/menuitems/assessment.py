from nicegui import ui

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


def assessment_panel(panel, selected_menu):
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
            },
            'series': [{
                'type': 'radar',
                'data': [
                    {'value': list(p['scores'].values()), 'name': p['name']} for p in plans
                ]
            }]
        }).classes('w-full h-80 my-4')

        # 下方：指标分析图
        with ui.tabs() as tabs:
            for dim in dimensions:
                ui.tab(dim)

        with ui.tab_panels(tabs=tabs, value=dimensions[0]).classes('w-full'):
            ui.label("指标分析图")
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
                    }).classes('w-full h-80')
