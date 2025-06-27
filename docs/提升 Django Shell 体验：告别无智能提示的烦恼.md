# 提升 Django Shell 体验：告别无智能提示的烦恼

`python manage.py shell` 是 Django 开发中不可或缺的工具，但默认缺乏智能提示确实影响效率。以下是几种提升体验的解决方案：

## 解决方案概览

| 方法 | 难度 | 功能 | 推荐指数 |
|------|------|------|----------|
| IPython | ★☆☆ | 基本补全 | ⭐⭐⭐⭐ |
| django-extensions | ★★☆ | 自动导入模型 | ⭐⭐⭐⭐⭐ |
| ptpython | ★★☆ | 高级REPL | ⭐⭐⭐⭐ |
| IDE集成 | ★★★ | 完整IDE功能 | ⭐⭐⭐⭐⭐ |
| 自定义启动脚本 | ★★☆ | 个性化配置 | ⭐⭐⭐ |

## 具体实现方案

### 1. 使用 IPython - 最简解决方案

```bash
pip install ipython
```

之后运行 `python manage.py shell` 会自动使用 IPython，提供基本代码补全。

### 2. 使用 django-extensions - 开发者最爱

```bash
pip install django-extensions
```

在 `settings.py` 中添加：
```python
INSTALLED_APPS = [
    ...
    'django_extensions',
]
```

使用增强版 shell：
```bash
python manage.py shell_plus --ipython
```

**功能亮点**：
- 自动导入所有模型
- 支持历史命令记录
- 可配置自动导入常用模块

### 3. 使用 ptpython - 高级REPL体验

```bash
pip install ptpython
```

创建配置文件 `~/.ptpython/config.py`:
```python
from prompt_toolkit.styles import Style

def configure(repl):
    # 启用自动补全
    repl.enable_auto_suggest = True
    repl.enable_open_in_editor = True
    
    # 自定义样式
    repl.install_ui_colorscheme('my-style', Style.from_dict({
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00aaaa #000000',
        'scrollbar.background': 'bg:#88aaaa',
        'scrollbar.button': 'bg:#222222',
    }))
    repl.use_ui_colorscheme('my-style')
```

使用：
```bash
ptpython manage.py shell
```

### 4. IDE 集成 - 终极解决方案

#### VS Code 配置

1. 安装 Python 和 Django 扩展
2. 创建 `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django Shell",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["shell"],
            "console": "integratedTerminal",
            "django": true
        }
    ]
}
```

3. 按 F5 启动带智能提示的 Django shell

#### PyCharm 配置

1. 打开 "Run/Debug Configurations"
2. 添加新的 "Django Console" 配置
3. 设置 "Django project root" 和 "Manage script"
4. 启动后获得完整智能提示

### 5. 自定义启动脚本 - 个性化解决方案

创建 `shell_startup.py`:
```python
import sys
import django
from django.conf import settings
from django.db.models import *

# 自动导入常用模块和模型
__all__ = ['*']  # 允许导入所有内容

# 自动导入所有已安装app的模型
for app in settings.INSTALLED_APPS:
    try:
        app_name = app.split('.')[-1]
        app_module = __import__(f"{app}.models", fromlist=[app_name])
        for model_name in dir(app_module):
            model = getattr(app_module, model_name)
            if isinstance(model, type) and issubclass(model, django.db.models.Model):
                globals()[model_name] = model
    except ImportError:
        continue

# 添加常用快捷方式
qs = django.db.models.QuerySet
f = django.db.models.F
q = django.db.models.Q
```

在 `settings.py` 中添加：
```python
SHELL_PLUS_PRE_IMPORTS = [
    ('shell_startup', '*'),
]
```

使用：
```bash
python manage.py shell_plus
```

## 高级技巧：增强 Django Shell

### 1. 自动加载常用函数

在 `settings.py` 中添加：
```python
SHELL_PLUS_POST_IMPORTS = [
    ('datetime', ('datetime', 'timedelta')),
    ('json', ('loads', 'dumps')),
    ('pprint', 'pprint'),
]
```

### 2. 添加自定义魔术命令

创建 `custom_magics.py`:
```python
from IPython.core.magic import register_line_magic

@register_line_magic
def show_urls(line):
    """显示所有注册的URL"""
    from django.urls import get_resolver
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        print(pattern)
```

在 `settings.py` 中：
```python
SHELL_PLUS_MAGIC_IMPORTS = [
    'custom_magics',
]
```

### 3. 使用 Jupyter Notebook

```bash
pip install jupyter
python manage.py shell_plus --notebook
```

创建 `~/.jupyter/jupyter_notebook_config.py`:
```python
c.NotebookApp.contents_manager_class = 'jupytext.TextFileContentsManager'
c.ContentsManager.default_jupytext_formats = 'ipynb,py'
```

## 性能优化建议

对于大型项目，shell 启动慢的问题：
```bash
# 仅加载必要app
python manage.py shell_plus --notebook --dont-load app1,app2

# 使用缓存
pip install django-cacheops
```

## 最终推荐工作流

1. **日常开发**：使用 VS Code 或 PyCharm 的集成 Django Console
2. **快速调试**：`python manage.py shell_plus --ipython`
3. **数据分析**：`python manage.py shell_plus --notebook`
4. **生产调试**：`ptpython manage.py shell`（轻量级）

通过以上方法，你可以彻底告别 Django shell 无智能提示的时代，大幅提升开发效率和体验！
