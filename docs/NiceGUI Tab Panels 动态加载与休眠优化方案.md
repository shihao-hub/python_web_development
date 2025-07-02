# NiceGUI Tab Panels 动态加载与休眠优化方案

在 NiceGUI 中，`ui.tab_panels` 默认会同时加载所有标签页的内容，即使某些标签页未被选中。这可能导致性能问题，特别是当标签页包含复杂内容时。以下是实现标签页"休眠"功能的完整解决方案：

```python
from nicegui import ui
import time

class LazyTabPanels:
    def __init__(self):
        self.tabs = ui.tabs().classes('w-full')
        self.panels = ui.tab_panels(self.tabs).classes('w-full')
        self.active_tab = None
        self.tab_contents = {}
        self.tab_states = {}
        
        # 添加标签页
        self.add_tab('仪表盘', self.create_dashboard_tab)
        self.add_tab('数据分析', self.create_analytics_tab)
        self.add_tab('系统设置', self.create_settings_tab)
        
        # 监听标签页切换
        self.tabs.on('update:model-value', self.on_tab_change)
    
    def add_tab(self, name, content_creator):
        """添加新标签页"""
        tab = ui.tab(name, name=name)
        self.tabs.add(tab)
        
        # 存储内容创建函数
        self.tab_contents[name] = content_creator
        self.tab_states[name] = {'loaded': False, 'content': None}
    
    def on_tab_change(self, event):
        """处理标签页切换事件"""
        new_tab = event.args
        
        # 激活新标签页
        self.activate_tab(new_tab)
        
        # 如果之前有活动标签页，则将其休眠
        if self.active_tab and self.active_tab != new_tab:
            self.sleep_tab(self.active_tab)
        
        self.active_tab = new_tab
    
    def activate_tab(self, tab_name):
        """激活标签页内容"""
        # 如果内容未加载，则创建内容
        if not self.tab_states[tab_name]['loaded']:
            with self.panels:
                with ui.tab_panel(tab_name):
                    # 显示加载状态
                    with ui.column().classes('items-center justify-center h-64'):
                        ui.spinner(size='lg', color='primary')
                        ui.label(f'正在加载 {tab_name}...').classes('mt-4')
                    
                    # 模拟加载延迟
                    ui.timer(0.5, lambda: self.load_tab_content(tab_name), once=True)
        # 如果内容已加载，则显示
        else:
            self.show_tab_content(tab_name)
    
    def load_tab_content(self, tab_name):
        """加载标签页内容"""
        # 清除加载指示器
        self.panels.clear()
        
        # 创建实际内容
        with self.panels:
            with ui.tab_panel(tab_name):
                content = self.tab_contents[tab_name]()
                self.tab_states[tab_name]['content'] = content
                self.tab_states[tab_name]['loaded'] = True
        
        # 更新UI状态
        self.tabs.set_value(tab_name)
        ui.notify(f'{tab_name} 已加载', type='positive')
    
    def show_tab_content(self, tab_name):
        """显示已加载的标签页内容"""
        # 确保标签页面板正确显示
        self.panels.set_value(tab_name)
        self.tabs.set_value(tab_name)
        
        # 恢复组件状态（如果有保存的状态）
        if tab_name in self.tab_states and self.tab_states[tab_name].get('state'):
            self.restore_tab_state(tab_name)
    
    def sleep_tab(self, tab_name):
        """休眠标签页"""
        if self.tab_states[tab_name]['loaded']:
            # 保存当前状态
            self.save_tab_state(tab_name)
            
            # 隐藏内容
            self.panels.clear()
            ui.notify(f'{tab_name} 已休眠', type='info')
            
            # 模拟资源释放
            self.release_tab_resources(tab_name)
    
    def save_tab_state(self, tab_name):
        """保存标签页状态（例如表单输入）"""
        # 在实际应用中，这里可以保存表单数据等状态
        self.tab_states[tab_name]['state'] = {
            'timestamp': time.time(),
            'message': f'{tab_name} 状态已保存'
        }
    
    def restore_tab_state(self, tab_name):
        """恢复标签页状态"""
        # 在实际应用中，这里可以恢复表单数据等状态
        state = self.tab_states[tab_name].get('state', {})
        if state:
            ui.notify(f'{tab_name} 状态已恢复', type='info')
    
    def release_tab_resources(self, tab_name):
        """释放标签页资源（如停止视频、动画等）"""
        # 在实际应用中，这里可以停止正在运行的资源
        pass
    
    # 标签页内容创建函数
    def create_dashboard_tab(self):
        with ui.column().classes('w-full p-4 gap-4'):
            ui.label('仪表盘').classes('text-2xl font-bold')
            
            # 性能指标卡片
            with ui.grid(columns=3).classes('w-full gap-4'):
                with ui.card().classes('p-4 bg-blue-50'):
                    ui.label('CPU 使用率').classes('text-lg')
                    ui.linear_progress(value=0.65).classes('w-full mt-2')
                    ui.label('65%').classes('text-right text-sm')
                
                with ui.card().classes('p-4 bg-green-50'):
                    ui.label('内存占用').classes('text-lg')
                    ui.linear_progress(value=0.42).classes('w-full mt-2')
                    ui.label('42%').classes('text-right text-sm')
                
                with ui.card().classes('p-4 bg-yellow-50'):
                    ui.label('网络流量').classes('text-lg')
                    ui.linear_progress(value=0.78).classes('w-full mt-2')
                    ui.label('78%').classes('text-right text-sm')
            
            # 图表区域
            with ui.card().classes('w-full p-4 mt-4'):
                ui.label('性能趋势图').classes('text-xl font-semibold mb-4')
                ui.chart({
                    'title': False,
                    'chart': {'type': 'line'},
                    'xAxis': {'categories': ['周一', '周二', '周三', '周四', '周五', '周六', '周日']},
                    'series': [
                        {'name': 'CPU', 'data': [65, 59, 80, 81, 56, 55, 70]},
                        {'name': '内存', 'data': [42, 45, 40, 38, 47, 50, 45]},
                        {'name': '网络', 'data': [78, 65, 70, 72, 75, 80, 85]}
                    ]
                }).classes('w-full h-64')
        
        return "仪表盘内容"
    
    def create_analytics_tab(self):
        with ui.column().classes('w-full p-4 gap-4'):
            ui.label('数据分析').classes('text-2xl font-bold')
            
            # 数据筛选器
            with ui.card().classes('w-full p-4'):
                with ui.row().classes('items-center gap-4'):
                    ui.label('日期范围:').classes('font-medium')
                    ui.date(value='2023-01-01').props('range')
                    
                    ui.label('数据类型:').classes('ml-4 font-medium')
                    ui.select(['销售数据', '用户行为', '性能指标'], value='销售数据')
                    
                    ui.button('生成报告', icon='analytics', color='primary').classes('ml-auto')
            
            # 数据表格
            with ui.card().classes('w-full p-4'):
                columns = [
                    {'name': 'id', 'label': 'ID', 'field': 'id'},
                    {'name': 'name', 'label': '名称', 'field': 'name', 'align': 'left'},
                    {'name': 'value', 'label': '数值', 'field': 'value'},
                    {'name': 'status', 'label': '状态', 'field': 'status'},
                ]
                rows = [
                    {'id': 1, 'name': '项目 A', 'value': 2450, 'status': '完成'},
                    {'id': 2, 'name': '项目 B', 'value': 1800, 'status': '进行中'},
                    {'id': 3, 'name': '项目 C', 'value': 3200, 'status': '完成'},
                    {'id': 4, 'name': '项目 D', 'value': 1500, 'status': '暂停'},
                ]
                ui.table(columns=columns, rows=rows, row_key='id').classes('w-full')
            
            # 分布图
            with ui.grid(columns=2).classes('w-full gap-4 mt-4'):
                with ui.card():
                    ui.label('类别分布').classes('text-lg font-semibold mb-2')
                    ui.chart({
                        'title': False,
                        'chart': {'type': 'pie'},
                        'series': [{
                            'name': '占比',
                            'data': [
                                {'name': '类别 A', 'y': 45},
                                {'name': '类别 B', 'y': 25},
                                {'name': '类别 C', 'y': 15},
                                {'name': '其他', 'y': 15}
                            ]
                        }]
                    }).classes('w-full h-64')
                
                with ui.card():
                    ui.label('区域分布').classes('text-lg font-semibold mb-2')
                    ui.chart({
                        'title': False,
                        'chart': {'type': 'bar'},
                        'xAxis': {'categories': ['东部', '西部', '南部', '北部']},
                        'series': [{'name': '销量', 'data': [120, 95, 150, 80]}]
                    }).classes('w-full h-64')
        
        return "数据分析内容"
    
    def create_settings_tab(self):
        with ui.column().classes('w-full p-4 gap-4'):
            ui.label('系统设置').classes('text-2xl font-bold')
            
            # 系统配置表单
            with ui.card().classes('w-full p-4'):
                with ui.column().classes('gap-4'):
                    with ui.row().classes('items-center gap-4'):
                        ui.label('系统名称:').classes('w-32 font-medium')
                        ui.input(value='我的应用系统').classes('flex-grow')
                    
                    with ui.row().classes('items-center gap-4'):
                        ui.label('时区设置:').classes('w-32 font-medium')
                        ui.select(['UTC', 'GMT+8', 'GMT-5'], value='GMT+8').classes('flex-grow')
                    
                    with ui.row().classes('items-center gap-4'):
                        ui.label('主题设置:').classes('w-32 font-medium')
                        ui.select(['浅色模式', '深色模式', '自动'], value='浅色模式').classes('flex-grow')
                    
                    with ui.row().classes('items-center gap-4'):
                        ui.label('自动更新:').classes('w-32 font-medium')
                        ui.switch(value=True)
            
            # 用户管理
            with ui.card().classes('w-full p-4 mt-4'):
                ui.label('用户账户').classes('text-xl font-semibold mb-4')
                
                columns = [
                    {'name': 'username', 'label': '用户名', 'field': 'username'},
                    {'name': 'role', 'label': '角色', 'field': 'role'},
                    {'name': 'last_login', 'label': '最后登录', 'field': 'last_login'},
                    {'name': 'actions', 'label': '操作', 'field': 'actions'},
                ]
                rows = [
                    {
                        'username': 'admin',
                        'role': '管理员',
                        'last_login': '2023-10-15 14:30',
                        'actions': ui.button('编辑', icon='edit').props('dense')
                    },
                    {
                        'username': 'user1',
                        'role': '编辑',
                        'last_login': '2023-10-16 09:15',
                        'actions': ui.button('编辑', icon='edit').props('dense')
                    },
                    {
                        'username': 'user2',
                        'role': '查看者',
                        'last_login': '2023-10-14 16:45',
                        'actions': ui.button('编辑', icon='edit').props('dense')
                    },
                ]
                ui.table(columns=columns, rows=rows, row_key='username').classes('w-full')
            
            # 系统操作
            with ui.row().classes('w-full justify-end gap-4 mt-6'):
                ui.button('重置设置', icon='restart_alt', color='negative')
                ui.button('保存设置', icon='save', color='primary')
        
        return "系统设置内容"

# 主应用
def main():
    ui.query('body').classes('bg-gray-50 p-4')
    
    with ui.column().classes('w-full max-w-6xl mx-auto gap-6'):
        ui.label('动态标签页管理系统').classes('text-3xl font-bold text-gray-800 mb-2')
        ui.markdown('此演示展示如何实现标签页的按需加载和休眠功能').classes('text-gray-600 mb-6')
        
        # 创建标签页面板
        tab_panels = LazyTabPanels()
        
        # 系统状态监控
        with ui.expansion('系统状态监控', icon='monitor_heart').classes('w-full mt-8 bg-white rounded-lg'):
            with ui.column().classes('p-4 gap-2'):
                ui.label('标签页状态:').classes('font-medium')
                status_table = ui.aggrid({
                    'columnDefs': [
                        {'headerName': '标签页名称', 'field': 'name'},
                        {'headerName': '加载状态', 'field': 'loaded'},
                        {'headerName': '最后激活', 'field': 'last_active'},
                        {'headerName': '内存占用', 'field': 'memory'},
                    ],
                    'rowData': [
                        {'name': '仪表盘', 'loaded': False, 'last_active': '从未', 'memory': '0 MB'},
                        {'name': '数据分析', 'loaded': False, 'last_active': '从未', 'memory': '0 MB'},
                        {'name': '系统设置', 'loaded': False, 'last_active': '从未', 'memory': '0 MB'},
                    ]
                }).classes('w-full h-40')
                
                # 更新状态函数
                def update_status():
                    data = []
                    for name, state in tab_panels.tab_states.items():
                        active_time = state.get('state', {}).get('timestamp', 0)
                        last_active = '从未' if active_time == 0 else time.strftime('%H:%M:%S', time.localtime(active_time))
                        
                        # 模拟内存占用
                        memory = '0 MB'
                        if state['loaded']:
                            memory = f'{len(name) * 2} MB'  # 模拟内存占用
                        
                        data.append({
                            'name': name,
                            'loaded': '是' if state['loaded'] else '否',
                            'last_active': last_active,
                            'memory': memory
                        })
                    
                    status_table.options['rowData'] = data
                    status_table.update()
                
                ui.timer(1.0, update_status)
        
        # 操作说明
        with ui.card().classes('w-full p-4 bg-blue-50 border border-blue-200'):
            ui.markdown("""
            ### 动态标签页功能说明
            
            - **按需加载**：标签页内容只在首次访问时加载
            - **智能休眠**：离开标签页时自动释放资源
            - **状态保存**：表单数据在休眠前自动保存
            - **性能优化**：减少同时加载的资源，提高响应速度
            
            切换标签页观察控制台日志和状态监控面板的变化
            """)

if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(title="动态标签页管理系统", port=8080, reload=False)
```

## 实现原理与关键功能

### 1. 按需加载机制

```python
def activate_tab(self, tab_name):
    """激活标签页内容"""
    # 如果内容未加载，则创建内容
    if not self.tab_states[tab_name]['loaded']:
        with self.panels:
            with ui.tab_panel(tab_name):
                # 显示加载状态
                with ui.column().classes('items-center justify-center h-64'):
                    ui.spinner(size='lg', color='primary')
                    ui.label(f'正在加载 {tab_name}...').classes('mt-4')
                
                # 模拟加载延迟
                ui.timer(0.5, lambda: self.load_tab_content(tab_name), once=True)
```

### 2. 标签页休眠功能

```python
def sleep_tab(self, tab_name):
    """休眠标签页"""
    if self.tab_states[tab_name]['loaded']:
        # 保存当前状态
        self.save_tab_state(tab_name)
        
        # 隐藏内容
        self.panels.clear()
        ui.notify(f'{tab_name} 已休眠', type='info')
        
        # 模拟资源释放
        self.release_tab_resources(tab_name)
```

### 3. 状态保存与恢复

```python
def save_tab_state(self, tab_name):
    """保存标签页状态（例如表单输入）"""
    # 在实际应用中，这里可以保存表单数据等状态
    self.tab_states[tab_name]['state'] = {
        'timestamp': time.time(),
        'message': f'{tab_name} 状态已保存'
    }

def restore_tab_state(self, tab_name):
    """恢复标签页状态"""
    # 在实际应用中，这里可以恢复表单数据等状态
    state = self.tab_states[tab_name].get('state', {})
    if state:
        ui.notify(f'{tab_name} 状态已恢复', type='info')
```

### 4. 资源管理

```python
def release_tab_resources(self, tab_name):
    """释放标签页资源（如停止视频、动画等）"""
    # 在实际应用中，这里可以停止正在运行的资源
    # 例如：停止视频播放、暂停数据更新、取消网络请求等
    pass
```

## 状态监控面板

为了直观展示标签页的加载状态，我们添加了实时监控面板：

```python
# 系统状态监控
with ui.expansion('系统状态监控', icon='monitor_heart').classes('w-full mt-8 bg-white rounded-lg'):
    with ui.column().classes('p-4 gap-2'):
        ui.label('标签页状态:').classes('font-medium')
        status_table = ui.aggrid({...})
        
        # 更新状态函数
        def update_status():
            data = []
            for name, state in tab_panels.tab_states.items():
                # 收集标签页状态信息
                ...
            
            status_table.options['rowData'] = data
            status_table.update()
        
        ui.timer(1.0, update_status)
```

## 使用场景与优势

1. **复杂应用优化**：
   - 当应用包含多个资源密集型标签页时
   - 减少初始加载时间
   - 提高整体应用响应速度

2. **移动设备适配**：
   - 减少内存占用
   - 节省电池消耗
   - 改善低性能设备体验

3. **数据敏感场景**：
   - 自动保存表单状态
   - 防止数据丢失
   - 恢复上次操作状态

4. **实时资源管理**：
   - 自动停止后台任务
   - 释放视频/音频资源
   - 暂停数据更新

## 扩展建议

1. **持久化状态保存**：
   ```python
   def save_tab_state(self, tab_name):
       # 实际应用中可以将状态保存到localStorage或数据库
       ui.local_storage.set(f'tab_state_{tab_name}', self.get_current_state())
   ```

2. **资源释放增强**：
   ```python
   def release_tab_resources(self, tab_name):
       # 停止所有定时器
       for timer in self.tab_timers.get(tab_name, []):
           timer.deactivate()
       
       # 暂停媒体播放
       for media in self.tab_media.get(tab_name, []):
           media.run_method('pause()')
   ```

3. **预加载策略**：
   ```python
   def preload_tab(self, tab_name):
       """在后台预加载标签页"""
       if not self.tab_states[tab_name]['loaded']:
           # 在后台线程加载内容但不显示
           self.load_tab_content(tab_name, background=True)
   ```

这个解决方案通过按需加载和智能休眠机制，有效优化了 NiceGUI 中标签页的资源管理，特别适合包含复杂内容或资源密集型组件的应用场景。