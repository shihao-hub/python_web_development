# NiceGUI Tree 组件参数详解

`Tree` 组件是 NiceGUI 中用于展示树形结构数据的强大组件，特别适合展示层级数据（如文件系统、组织结构等）。下面我将详细解释 Tree 组件的各个参数及其用法：

## 参数详解

### 1. `nodes: List[Dict]`
- **作用**：树形结构的数据源
- **要求**：
  - 必须是字典列表
  - 每个字典代表一个节点
  - 节点应包含标识符、标签和子节点信息
- **示例**：
  ```python
  nodes = [
      {
          'id': 'root',
          'label': 'Root Node',
          'children': [
              {'id': 'child1', 'label': 'Child 1'},
              {'id': 'child2', 'label': 'Child 2'}
          ]
      }
  ]
  ```

### 2. `node_key: str = 'id'`
- **作用**：指定节点唯一标识符的键名
- **默认值**：'id'
- **注意**：
  - 这个值必须在整个树中唯一
  - 用于事件处理和节点操作
- **示例**：
  ```python
  # 使用 'key' 作为标识符键名
  ui.tree(nodes, node_key='key')
  ```

### 3. `label_key: str = 'label'`
- **作用**：指定节点显示文本的键名
- **默认值**：'label'
- **示例**：
  ```python
  # 使用 'name' 作为显示文本键名
  ui.tree(nodes, label_key='name')
  ```

### 4. `children_key: str = 'children'`
- **作用**：指定子节点列表的键名
- **默认值**：'children'
- **注意**：
  - 如果节点没有子节点，可以省略此键或设为空列表
- **示例**：
  ```python
  # 使用 'items' 作为子节点键名
  ui.tree(nodes, children_key='items')
  ```

### 5. `on_select: Optional[Handler] = None`
- **作用**：节点选中事件回调函数
- **事件参数**：`ValueChangeEventArguments`
  - `value`: 选中的节点 ID
  - `previous_value`: 之前选中的节点 ID
- **示例**：
  ```python
  def handle_select(e: ValueChangeEventArguments):
      ui.notify(f'Selected node: {e.value}')
  
  ui.tree(nodes, on_select=handle_select)
  ```

### 6. `on_expand: Optional[Handler] = None`
- **作用**：节点展开/折叠事件回调函数
- **事件参数**：`ValueChangeEventArguments`
  - `value`: 展开/折叠的节点 ID
  - `args`: 包含展开状态 (expanded)
- **示例**：
  ```python
  def handle_expand(e: ValueChangeEventArguments):
      action = 'expanded' if e.args['expanded'] else 'collapsed'
      ui.notify(f'Node {e.value} {action}')
  
  ui.tree(nodes, on_expand=handle_expand)
  ```

### 7. `on_tick: Optional[Handler] = None`
- **作用**：节点勾选状态变化事件回调函数
- **事件参数**：`ValueChangeEventArguments`
  - `value`: 所有被勾选的节点 ID 列表
- **注意**：
  - 需要启用勾选功能（通常需要设置 `tick_strategy`）
- **示例**：
  ```python
  def handle_tick(e: ValueChangeEventArguments):
      ui.notify(f'Ticked nodes: {e.value}')
  
  ui.tree(nodes, on_tick=handle_tick, tick_strategy='leaf')
  ```

### 8. `tick_strategy: Optional[Literal] = None`
- **作用**：定义节点勾选策略
- **可选值**：
  - `'leaf'`: 只勾选叶子节点（无子节点的节点）
  - `'leaf-filtered'`: 只勾选过滤后可见的叶子节点
  - `'strict'`: 严格模式，节点独立勾选（不关联父子节点）
- **注意**：
  - 当设置此参数时，会自动显示勾选框
- **示例**：
  ```python
  # 启用叶子节点勾选策略
  ui.tree(nodes, tick_strategy='leaf')
  ```

## 完整使用示例

```python
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

# 树形结构数据
tree_data = [
    {
        'id': 'company',
        'name': 'Company Structure',
        'items': [
            {
                'id': 'management',
                'name': 'Management',
                'items': [
                    {'id': 'ceo', 'name': 'CEO'},
                    {'id': 'cto', 'name': 'CTO'}
                ]
            },
            {
                'id': 'development',
                'name': 'Development',
                'items': [
                    {'id': 'frontend', 'name': 'Frontend Team'},
                    {'id': 'backend', 'name': 'Backend Team'}
                ]
            }
        ]
    },
    {
        'id': 'projects',
        'name': 'Projects',
        'items': [
            {'id': 'project1', 'name': 'Project Alpha'},
            {'id': 'project2', 'name': 'Project Beta'}
        ]
    }
]

def handle_select(e: ValueChangeEventArguments):
    ui.notify(f'✅ Selected node: {e.value}')

def handle_expand(e: ValueChangeEventArguments):
    action = '展开' if e.args['expanded'] else '折叠'
    ui.notify(f'📂 Node {e.value} {action}')

def handle_tick(e: ValueChangeEventArguments):
    ui.notify(f'☑️ Ticked nodes: {e.value}')

with ui.card().classes('w-full max-w-2xl mx-auto my-4'):
    ui.label('公司组织结构树').classes('text-2xl font-bold mb-4')
    
    # 创建树组件
    tree = ui.tree(
        nodes=tree_data,
        node_key='id',
        label_key='name',
        children_key='items',
        on_select=handle_select,
        on_expand=handle_expand,
        on_tick=handle_tick,
        tick_strategy='leaf'  # 启用勾选功能
    ).classes('w-full')
    
    # 添加控制按钮
    with ui.row().classes('mt-4 gap-2'):
        ui.button('展开所有', on_click=lambda: tree.props('expanded-all')).classes('bg-green-500 text-white')
        ui.button('折叠所有', on_click=lambda: tree.props(expanded_all=False)).classes('bg-blue-500 text-white')
        ui.button('选择开发部', on_click=lambda: tree.props(selected='development')).classes('bg-purple-500 text-white')
        ui.button('获取勾选项', on_click=lambda: ui.notify(f'当前勾选: {tree._props["ticked"]}')).classes('bg-yellow-500 text-black')

ui.run()
```

## 高级功能与技巧

### 1. 动态更新树结构
```python
# 添加节点
def add_node():
    new_node = {'id': 'new', 'label': 'New Node'}
    tree_data.append(new_node)
    tree.update()

# 删除节点
def remove_node():
    if tree_data:
        tree_data.pop()
        tree.update()
```

### 2. 自定义节点渲染
```python
tree = ui.tree(nodes).classes('w-full')

# 自定义节点插槽
with tree.add_slot('default-header'):
    # 自定义节点内容
    ui.icon('folder').classes('text-yellow-400')
    ui.label('{{ props.node.label }}').classes('ml-2')
```

### 3. 搜索过滤功能
```python
search = ui.input('搜索节点').classes('w-full')

@search.on('input')
def filter_tree():
    # 实现过滤逻辑
    tree.props('filter', search.value)
```

### 4. 拖放功能支持
```python
tree.props('draggable')
tree.props('drop-mode')

# 处理拖放事件
def handle_drop(e):
    ui.notify(f'节点 {e.args["node"]} 移动到 {e.args["target"]}')
    
tree.on('drop', handle_drop)
```

## 常见问题解决

1. **节点无法展开/折叠**
   - 确保包含子节点的节点有 `children_key` 指定的属性
   - 检查数据格式是否正确

2. **勾选状态不联动**
   - 确认设置了 `tick_strategy` 参数
   - 检查数据结构是否符合策略要求

3. **事件不触发**
   - 确保使用了正确的事件名称
   - 检查事件处理函数签名是否正确

4. **性能问题**
   - 对于大型树结构，使用虚拟滚动：
     ```python
     tree.props('virtual-scroll')
     ```

Tree 组件是 NiceGUI 中最复杂的组件之一，但提供了强大的树形数据展示能力。通过合理使用上述参数和技巧，您可以创建出功能丰富的树形结构界面。
