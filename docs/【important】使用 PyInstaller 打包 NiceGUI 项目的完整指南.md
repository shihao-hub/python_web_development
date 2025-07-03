# 使用 PyInstaller 打包 NiceGUI 项目的完整指南

PyInstaller 是打包 Python 应用为独立可执行文件的强大工具。对于 NiceGUI 项目，由于其 Web 特性和依赖关系，打包需要特别注意。下面是一步一步的详细指南：

## 基础打包步骤

### 1. 创建示例应用
```python
# main.py
from nicegui import ui

ui.label("Hello NiceGUI!")
ui.button("Click me", on_click=lambda: ui.notify("Button clicked!"))

# 注意：打包时使用单进程模式
ui.run(reload=False, native=True, single_process=True)
```

### 2. 安装 PyInstaller
```bash
pip install pyinstaller
```

### 3. 基础打包命令
```bash
pyinstaller --name myapp --onefile --add-data "venv/Lib/site-packages/nicegui;nicegui" main.py
```

**关键参数说明：**
- `--onefile`: 创建单个可执行文件
- `--add-data`: 添加 NiceGUI 的静态资源文件
- `--name`: 指定输出文件名

## 完整打包解决方案

### 创建打包配置文件 (build.spec)
```python
# build.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('venv/Lib/site-packages/nicegui/static', 'nicegui/static'),
        ('venv/Lib/site-packages/nicegui/elements', 'nicegui/elements'),
    ],
    hiddenimports=[
        'pkg_resources.py2_warn',
        'nicegui.elements',
        'nicegui.dependencies',
        'uvicorn.protocols.http',
        'uvicorn.protocols.websockets',
        'uvicorn.loops',
        'uvicorn.loops.auto'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='myapp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 设为 False 可隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='myapp',
)
```

### 优化后的打包命令
```bash
pyinstaller build.spec
```

## 解决常见问题

### 1. 处理静态资源文件
NiceGUI 需要访问其静态文件（CSS、JS 等）。确保正确添加：

```python
# 在 spec 文件中
datas=[
    (os.path.join(site_packages, 'nicegui', 'static'), 'nicegui/static'),
    (os.path.join(site_packages, 'nicegui', 'elements'), 'nicegui/elements'),
]
```

### 2. 处理隐藏导入
NiceGUI 依赖的某些模块需要显式导入：

```python
hiddenimports=[
    'uvicorn.protocols.http',
    'uvicorn.protocols.websockets',
    'uvicorn.loops.auto',
    'uvicorn.loops',
    'asyncio.windows_events',
    'nicegui.dependencies',
    'nicegui.elements',
    'pkg_resources.py2_warn'
]
```

### 3. 处理 WebView2 运行时问题
如果使用 `native=True`，确保目标系统安装 WebView2 Runtime：

```python
# 在应用启动时检查
import sys
import os
import ctypes

def check_webview2():
    try:
        # 尝试加载 WebView2 库
        ctypes.windll.WebView2Loader
        return True
    except OSError:
        return False

if not check_webview2():
    print("WebView2 Runtime not found. Installing...")
    # 从应用目录中运行 WebView2 安装程序
    os.system(rf"{sys._MEIPASS}\MicrosoftEdgeWebview2Setup.exe")
```

### 4. 处理路径问题
打包后路径会改变，需要特殊处理资源路径：

```python
# 在 main.py 中添加
import sys
import os

def resource_path(relative_path):
    """获取资源的绝对路径"""
    try:
        # PyInstaller 创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# 设置静态文件路径
os.environ["NICEGUI_STATIC_DIRECTORY"] = resource_path("nicegui/static")
```

### 5. 处理多进程问题
打包后多进程可能无法工作，使用单进程模式：

```python
ui.run(reload=False, single_process=True)
```

## 高级打包技巧

### 1. 添加图标
```python
exe = EXE(
    # ...其他参数...
    icon='app_icon.ico',
)
```

### 2. 添加版本信息
创建 version.txt:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
          '040904B0',
          [StringStruct('CompanyName', 'Your Company'),
           StringStruct('FileDescription', 'NiceGUI Application'),
           StringStruct('FileVersion', '1.0.0'),
           StringStruct('InternalName', 'MyApp'),
           StringStruct('LegalCopyright', 'Copyright © 2023'),
           StringStruct('OriginalFilename', 'MyApp.exe'),
           StringStruct('ProductName', 'NiceGUI App'),
           StringStruct('ProductVersion', '1.0.0')])
      ]), 
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
```

在 spec 文件中添加：
```python
exe = EXE(
    # ...其他参数...
    version='version.txt',
)
```

### 3. 减小打包体积
```bash
pip install pyinstaller[encryption]  # 安装 UPX
```

在 spec 文件中启用 UPX：
```python
exe = EXE(
    # ...其他参数...
    upx=True,
    upx_exclude=[],  # 排除某些文件
)
```

### 4. 打包为单目录模式（推荐用于调试）
```bash
pyinstaller --name myapp --onedir main.py
```

## 完整打包脚本

```bash
#!/bin/bash
# build.sh

# 1. 清理旧构建
rm -rf build dist

# 2. 安装依赖
pip install -r requirements.txt

# 3. 生成版本信息
cat > version.txt <<EOL
VSVersionInfo(
  ... # 如上版本信息
)
EOL

# 4. 下载 WebView2 安装程序
curl -L -o MicrosoftEdgeWebview2Setup.exe "https://go.microsoft.com/fwlink/p/?LinkId=2124703"

# 5. 运行 PyInstaller
pyinstaller \
    --name myapp \
    --onefile \
    --add-data "venv/Lib/site-packages/nicegui/static;nicegui/static" \
    --add-data "venv/Lib/site-packages/nicegui/elements;nicegui/elements" \
    --add-data "MicrosoftEdgeWebview2Setup.exe;." \
    --hidden-import "uvicorn.protocols.http" \
    --hidden-import "uvicorn.protocols.websockets" \
    --hidden-import "uvicorn.loops.auto" \
    --hidden-import "uvicorn.loops" \
    --hidden-import "asyncio.windows_events" \
    --hidden-import "nicegui.dependencies" \
    --hidden-import "nicegui.elements" \
    --hidden-import "pkg_resources.py2_warn" \
    --icon app_icon.ico \
    --version-file version.txt \
    main.py

# 6. 清理临时文件
rm version.txt
```

## 测试打包后的应用

1. 在命令行运行：
   ```bash
   dist/myapp.exe
   ```

2. 检查：
   - 应用是否正常启动
   - 界面是否显示正确
   - 按钮点击等交互是否正常
   - 控制台是否有错误输出

## 处理常见错误

**问题：** 静态文件加载失败  
**解决：** 确保 `--add-data` 路径正确，使用 `sys._MEIPASS` 处理路径

**问题：** 模块找不到错误  
**解决：** 在 `hiddenimports` 中添加缺失模块

**问题：** WebView2 初始化失败  
**解决：** 打包 WebView2 安装程序并在启动时检查安装

**问题：** 应用启动后立即退出  
**解决：** 确保使用 `single_process=True` 和 `reload=False`

**问题：** 打包文件过大  
**解决：**
- 使用 UPX 压缩
- 排除不必要的包
- 使用虚拟环境减少依赖

## 跨平台注意事项

### Linux/Mac 打包
```bash
# Linux
pyinstaller --name myapp --onefile --add-data "$(python -c 'import nicegui; print(nicegui.__path__[0])')/static:nicegui/static" main.py

# Mac
pyinstaller --name myapp --onefile --windowed --add-data "$(python -c 'import nicegui; print(nicegui.__path__[0])')/static:nicegui/static" main.py
```

### Mac 应用签名
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name (XXXXXXXXXX)" dist/myapp.app
```

## 总结

打包 NiceGUI 项目需要注意：
1. **静态资源**：正确添加 NiceGUI 的静态文件
2. **隐藏导入**：显式声明所有需要的模块
3. **单进程模式**：使用 `single_process=True`
4. **WebView2 处理**：包含安装程序或检查运行时
5. **路径处理**：使用 `sys._MEIPASS` 获取正确资源路径

按照这个指南，你应该能够成功打包 NiceGUI 应用。如果遇到特定问题，可以检查 PyInstaller 生成的 warn.txt 文件获取更多线索。
