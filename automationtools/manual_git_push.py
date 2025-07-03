"""
### 需求背景
对于所有被改动的文件，一次只能提交一个文件，而且每次都需要手动复制文件名和文件内容，非常麻烦。

为此我希望有这样一个功能的程序：

界面展示的是当前项目的目录树，但是这个目录树只展示蓝色和绿色的文件，蓝色文件表示该文件被修改过，绿色文件表示该文件被新增过。

对于每个子节点，右侧存在两个按钮，一个是复制文件名，一个是复制文件内容。


"""

import os
import subprocess
from dataclasses import dataclass
from typing import Literal, List, Tuple
from pathlib import Path

from loguru import logger

from nicegui import ui
from nicegui.events import ValueChangeEventArguments

ROOT_DIR = Path(__file__).resolve().parent.parent

# todo: 需要实现一个 map 类，可以根据 key 获得 value，也可以根据 value 获得 key
#       当然需要注意的是，一个 key 可能存在相等的 value，所以逆置后的 dict 的 value' 类型是 list/set
STATUS_TO_COLOR = {
    "added": "green",
    "modified": "blue",
}


@dataclass
class GitFileInfo:
    color: Literal["blue", "green"]
    filename: str
    filepath: str
    content: str


def get_all_files() -> List[GitFileInfo]:
    pass


# todo: 明确的需求说明非常重要，就上面的需求背景，deepseek 迅速生成了我所需要的内容（这次生成的很不错，能不能分析一下原因？）
#       太强了！几乎无错误，我的天。

def get_git_status() -> List[Tuple[str, str]]:
    """获取当前 Git 仓库的变更状态"""
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    logger.debug("the result of `git status --porcelain`:\n{}", result.stdout)
    if result.returncode != 0:
        return []

    status_lines = result.stdout.strip().split('\n')
    status_map = []

    for line in status_lines:
        if not line.strip():
            continue

        status_code = line[:2].strip()
        file_path = line[3:]

        # 解析状态
        if status_code in ('M', 'MM'):  # 修改的文件
            status_map.append(('modified', file_path))
        elif status_code in ('A', 'AM'):  # 新增的文件
            status_map.append(('added', file_path))
        elif status_code == '??':  # 未跟踪的文件（视为新增）
            status_map.append(('added', file_path))
        elif status_code == 'R':  # 重命名的文件
            old_path, new_path = file_path.split(' -> ')
            status_map.append(('renamed', new_path, old_path))
        elif status_code == 'D':  # 删除的文件
            status_map.append(('deleted', file_path))
    logger.debug("status_map:\n{}", status_map)
    return status_map


def build_file_tree(status_map):
    """构建包含状态的文件树结构"""
    tree = {}

    for status in status_map:
        file_path = status[1]
        path_parts = Path(file_path).parts

        current_level = tree
        for i, part in enumerate(path_parts):
            if part not in current_level:
                # 如果是最后一部分，说明是文件
                is_file = i == len(path_parts) - 1
                current_level[part] = {
                    'name': part,
                    'path': os.path.join(*path_parts[:i + 1]),
                    'children': {},
                    'is_file': is_file,
                    'status': status[0] if is_file else None
                }
            current_level = current_level[part]['children']
    logger.debug("tree: {}", tree)
    return tree


def convert_to_nicegui_tree(tree, parent_path=''):
    """将树结构转换为 NiceGUI 树组件需要的格式"""
    nodes = []

    for name, node in tree.items():
        full_path = node['path']
        nicegui_node = {
            'id': full_path,
            'label': name,
            'status': node['status'],
            'is_file': node['is_file'],
            'children': convert_to_nicegui_tree(node['children'], full_path)
        }
        nodes.append(nicegui_node)
    logger.debug("nodes:\n{}", nodes)
    return nodes


def create_file_node(node):
    """创建带有操作按钮的文件节点"""
    with ui.row().classes('items-center w-full justify-between hover:bg-gray-100 p-1 rounded'):
        # 文件图标和名称
        with ui.row().classes('items-center gap-2'):
            if node['is_file']:
                icon = 'description'
                color = 'text-blue-500' if node['status'] == 'modified' else 'text-green-500'
            else:
                icon = 'folder'
                color = 'text-gray-500'

            ui.icon(icon).classes(f'{color}').style('min-width: 24px')
            ui.label(node['label']).classes('font-mono text-sm')

        # 文件操作按钮
        if node['is_file']:
            with ui.row().classes('gap-1'):
                # 复制文件名按钮
                ui.button(icon='content_copy', on_click=lambda _, p=node['id']: copy_file_name(p)) \
                    .props('flat dense size=sm') \
                    .classes('text-blue-500 hover:bg-blue-100') \
                    .tooltip('复制文件名')

                # 复制文件内容按钮
                ui.button(icon='content_paste', on_click=lambda _, p=node['id']: copy_file_content(p)) \
                    .props('flat dense size=sm') \
                    .classes('text-green-500 hover:bg-green-100') \
                    .tooltip('复制文件内容')
    ui.separator().classes('w-full my-1')


async def copy_file_name(file_path):
    """复制文件名到剪贴板"""
    file_name = os.path.basename(file_path)
    await ui.run_javascript(f'navigator.clipboard.writeText("{file_name}")')
    ui.notify(f'已复制文件名: {file_name}', type='positive')


async def copy_file_content(file_path):
    """复制文件内容到剪贴板"""
    try:
        # todo: cache?
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 处理特殊字符
        escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
        await ui.run_javascript(f'navigator.clipboard.writeText(`{escaped_content}`)')
        ui.notify(f'已复制文件内容: {os.path.basename(file_path)}', type='positive')
    except Exception as e:
        ui.notify(f'复制文件内容失败: {str(e)}', type='negative')


def refresh_tree():
    """刷新文件树"""
    global file_tree_container, status_map

    # 清除旧内容
    file_tree_container.clear()

    # 获取新状态
    status_map = get_git_status()
    if not status_map:
        file_tree_container.clear()
        with file_tree_container:
            ui.label('没有检测到文件变更').classes('text-gray-500 text-lg')
        return

    # 构建新树
    file_tree = build_file_tree(status_map)
    nicegui_tree = convert_to_nicegui_tree(file_tree)

    # 显示新树
    with file_tree_container:
        for node in nicegui_tree:
            create_tree_node(node)


# temp
tree_nodes: List[ui.expansion] = []


def create_tree_node(node):
    """递归创建树节点"""
    if node['is_file']:
        create_file_node(node)
    else:
        with ui.expansion(node['label'], icon='folder').classes('w-full') as tree_node:
            tree_nodes.append(tree_node)
            for child in node['children']:
                create_tree_node(child)


@ui.page("/")
def main():
    """主界面"""
    global file_tree_container, status_map

    # 创建应用
    ui.add_head_html('''
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f7fa;
            }
            .nicegui-container {
                max-width: 1000px;
                margin: 0 auto;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                overflow: hidden;
            }
            .file-node {
                transition: background-color 0.2s;
            }
            .file-node:hover {
                background-color: #f0f7ff;
            }
        </style>
    ''')

    # with ui.card().classes('nicegui-container w-full p-0'):
    #     main()

    # 获取初始状态
    status_map = get_git_status()

    # 创建界面
    with ui.header().classes('bg-blue-800 text-white shadow-lg'):
        with ui.row().classes('items-center w-full justify-between'):
            ui.label('Git 变更文件管理').classes('text-2xl font-bold')
            with ui.row().classes('gap-2'):
                ui.button(icon='refresh', on_click=refresh_tree) \
                    .props('flat round') \
                    .classes('text-white hover:bg-blue-700') \
                    .tooltip('刷新文件树')

                ui.button(icon='help', on_click=lambda: ui.open('https://git-scm.com/docs/git-status')) \
                    .props('flat round') \
                    .classes('text-white hover:bg-blue-700') \
                    .tooltip('Git 状态文档')

    # 状态指示器
    with ui.row().classes('w-full bg-gray-100 p-2 justify-around items-center'):
        with ui.row().classes('items-center gap-2'):
            ui.icon('fiber_manual_record').classes('text-blue-500')
            ui.label('修改过的文件').classes('text-sm')

        with ui.row().classes('items-center gap-2'):
            ui.icon('fiber_manual_record').classes('text-green-500')
            ui.label('新增的文件').classes('text-sm')

    # 文件树容器
    global file_tree_container
    file_tree_container = ui.column().classes('w-full p-4 max-h-[70vh] overflow-y-auto')

    if not status_map:
        with file_tree_container:
            ui.label('没有检测到文件变更').classes('text-gray-500 text-lg')
    else:
        # 构建文件树
        file_tree = build_file_tree(status_map)
        nicegui_tree = convert_to_nicegui_tree(file_tree)

        with file_tree_container:
            for node in nicegui_tree:
                create_tree_node(node)

    # 统计信息
    modified_count = sum(1 for s in status_map if s[0] == 'modified')
    added_count = sum(1 for s in status_map if s[0] == 'added')

    with ui.footer().classes('bg-gray-100 p-2 text-center'):
        ui.label(f'总计: {len(status_map)} 个变更文件 (修改: {modified_count}, 新增: {added_count})') \
            .classes('text-gray-600')

    def expand_all():
        for _node in tree_nodes:
            _node.open()

    ui.timer(0.1, expand_all, once=True)


if __name__ in {'__main__', '__mp_main__'}:
    # 全局变量
    file_tree_container = None
    status_map = []

    ui.run(title='Git 变更文件管理器', host="localhost", port=14001, reload=False, show=False, favicon='📁')
