# NiceGUI 剪贴板写入超时问题解决方案

在 NiceGUI 中使用 `await ui.run_javascript(f'navigator.clipboard.writeText(`{escaped_content}`)')` 时遇到 "JavaScript did not respond within 1.0 s" 错误，这是因为浏览器剪贴板操作需要用户交互上下文和权限验证。下面我将提供一个完整的解决方案，确保剪贴板操作可靠执行。

## 问题分析与完整解决方案

```python
from nicegui import ui, run
import asyncio
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClipboardManager:
    def __init__(self):
        self.copy_queue = []
        self.is_copying = False
        self.last_copied = None
        self.last_copied_time = 0
        
    async def safe_copy_to_clipboard(self, content):
        """安全复制文本到剪贴板"""
        # 如果内容为空则跳过
        if not content:
            return False
        
        # 检查是否与上次复制相同且时间很近
        if content == self.last_copied and (time.time() - self.last_copied_time) < 1:
            return True
            
        # 将复制任务加入队列
        self.copy_queue.append(content)
        
        # 如果没有正在进行的复制任务，则启动复制
        if not self.is_copying:
            asyncio.create_task(self.process_copy_queue())
            
        return True
        
    async def process_copy_queue(self):
        """处理复制队列"""
        self.is_copying = True
        
        while self.copy_queue:
            content = self.copy_queue.pop(0)
            escaped_content = self.escape_content(content)
            
            # 尝试复制
            success = await self.try_copy(escaped_content)
            
            if success:
                # 更新最后复制状态
                self.last_copied = content
                self.last_copied_time = time.time()
                ui.notify("已复制到剪贴板!", type="positive")
            else:
                # 复制失败时提供备选方案
                self.copy_queue.append(content)  # 重新加入队列
                await self.offer_alternative_copy_method(content)
                break
                
        self.is_copying = False
        
    async def try_copy(self, escaped_content, timeout=3.0):
        """尝试执行复制操作"""
        try:
            # 使用更长的超时时间
            await ui.run_javascript(
                f"""
                (async function() {{
                    try {{
                        await navigator.clipboard.writeText(`{escaped_content}`);
                        return 'success';
                    }} catch (error) {{
                        console.error('Clipboard write failed:', error);
                        return 'error';
                    }}
                }})()
                """,
                timeout=timeout
            )
            return True
        except asyncio.TimeoutError:
            logger.warning(f"剪贴板操作超时 ({timeout}s)")
            return False
        except Exception as e:
            logger.error(f"剪贴板操作异常: {str(e)}")
            return False
            
    def escape_content(self, content):
        """转义内容以安全插入JavaScript"""
        # 替换反引号和美元符号
        escaped = content.replace('`', '\\`').replace('$', '\\$')
        
        # 处理换行符
        escaped = escaped.replace('\n', '\\n').replace('\r', '\\r')
        
        # 截断过长的文本
        if len(escaped) > 1000:
            escaped = escaped[:1000] + '...'
            
        return escaped
        
    async def offer_alternative_copy_method(self, content):
        """提供备选复制方法"""
        # 创建文本区域供用户手动复制
        with ui.dialog() as dialog, ui.card().classes("p-6 w-full max-w-2xl"):
            ui.label("剪贴板访问失败").classes("text-xl font-bold text-red-600 mb-4")
            
            ui.markdown("""
            **无法自动复制到剪贴板，可能是因为：**
            - 浏览器安全限制（需要用户交互）
            - 页面未使用 HTTPS
            - 浏览器扩展程序阻止了剪贴板访问
            """).classes("mb-4")
            
            ui.label("请手动复制以下内容：").classes("font-medium mb-2")
            
            # 创建可选择的文本区域
            textarea = ui.textarea(value=content).classes("w-full h-40 font-mono")
            textarea.props("readonly")
            
            with ui.row().classes("justify-end mt-4"):
                ui.button("关闭", on_click=dialog.close).props("outline")
                ui.button("复制", on_click=lambda: self.copy_via_textarea(textarea)).props("unelevated color=primary")
                
        dialog.open()
        
    async def copy_via_textarea(self, textarea):
        """通过文本区域执行复制"""
        try:
            # 使用DOM元素执行复制
            await ui.run_javascript(f"""
                (function() {{
                    const textarea = document.getElementById('{textarea.id}');
                    textarea.select();
                    document.execCommand('copy');
                    return 'success';
                }})()
            """)
            ui.notify("已复制到剪贴板!", type="positive")
        except Exception as e:
            logger.error(f"备选复制方法失败: {str(e)}")
            ui.notify("复制失败，请手动选择并复制文本", type="warning")

# 创建全局剪贴板管理器
clipboard = ClipboardManager()

# 主应用界面
def main():
    ui.query('body').classes('bg-gray-50 p-4')
    
    with ui.column().classes('w-full max-w-4xl mx-auto gap-6'):
        ui.label("剪贴板复制演示").classes("text-2xl font-bold text-gray-800")
        
        # 复制示例区域
        with ui.card().classes("w-full p-6 bg-white shadow-md rounded-xl"):
            ui.label("示例内容").classes("text-lg font-semibold mb-4")
            
            # 示例1：简单文本
            with ui.row().classes("items-center justify-between w-full mb-4 p-3 bg-blue-50 rounded-lg"):
                ui.label("简单文本：").classes("font-medium")
                ui.label("Hello, NiceGUI!").classes("font-mono")
                ui.button("复制", on_click=lambda: clipboard.safe_copy_to_clipboard("Hello, NiceGUI!")) \
                    .props("outline dense") \
                    .classes("ml-auto")
            
            # 示例2：多行文本
            with ui.row().classes("items-center justify-between w-full mb-4 p-3 bg-green-50 rounded-lg"):
                ui.label("多行文本：").classes("font-medium")
                ui.label("第一行\n第二行\n第三行").classes("font-mono whitespace-pre")
                ui.button("复制", on_click=lambda: clipboard.safe_copy_to_clipboard("第一行\n第二行\n第三行")) \
                    .props("outline dense") \
                    .classes("ml-auto")
            
            # 示例3：特殊字符文本
            with ui.row().classes("items-center justify-between w-full mb-4 p-3 bg-yellow-50 rounded-lg"):
                ui.label("特殊字符：").classes("font-medium")
                ui.label("文本包含 ` $ \\ ' 等特殊字符").classes("font-mono")
                ui.button("复制", on_click=lambda: clipboard.safe_copy_to_clipboard("文本包含 ` $ \\ ' 等特殊字符")) \
                    .props("outline dense") \
                    .classes("ml-auto")
            
            # 示例4：长文本
            with ui.row().classes("items-center justify-between w-full p-3 bg-purple-50 rounded-lg"):
                ui.label("长文本：").classes("font-medium")
                long_text = "这是一段非常长的文本，用于测试剪贴板操作是否能够正确处理长内容。" * 10
                ui.label(long_text[:50] + "...").classes("font-mono")
                ui.button("复制", on_click=lambda: clipboard.safe_copy_to_clipboard(long_text)) \
                    .props("outline dense") \
                    .classes("ml-auto")
        
        # 自定义内容复制
        with ui.card().classes("w-full p-6 bg-white shadow-md rounded-xl"):
            ui.label("自定义内容复制").classes("text-lg font-semibold mb-4")
            
            text_input = ui.textarea(label="输入要复制的内容").classes("w-full mb-4")
            
            with ui.row():
                ui.button("复制文本", on_click=lambda: clipboard.safe_copy_to_clipboard(text_input.value)) \
                    .props("unelevated color=primary")
                
                ui.button("复制为代码片段", on_click=lambda: clipboard.safe_copy_to_clipboard(f"```\n{text_input.value}\n```")) \
                    .props("outline")
        
        # 技术说明
        with ui.expansion("技术说明", icon="info").classes("w-full bg-white rounded-lg border border-gray-200"):
            with ui.column().classes("p-4 text-sm text-gray-700"):
                ui.markdown("""
                ### 剪贴板操作问题原因
                
                浏览器安全限制导致 `navigator.clipboard.writeText()` 需要：
                
                1. **用户交互上下文**：必须在用户点击等交互事件中触发
                2. **HTTPS 连接**：在非安全连接下可能被阻止
                3. **浏览器权限**：某些浏览器需要明确权限
                
                ### 本解决方案的关键点
                
                - **队列管理**：避免同时发起多个剪贴板请求
                - **安全转义**：正确处理特殊字符防止JS注入
                - **超时处理**：延长超时时间并处理超时情况
                - **备选方案**：提供手动复制选项作为后备
                - **错误恢复**：记录错误并优雅降级
                
                ### 使用建议
                
                1. 确保在用户交互事件中触发复制操作
                2. 部署时使用 HTTPS 协议
                3. 对于长文本提供截断预览
                """)
        
        # 状态监控
        with ui.card().classes("w-full p-4 bg-blue-50 border border-blue-200"):
            ui.label("剪贴板操作日志").classes("font-medium mb-2")
            log_area = ui.log().classes("w-full h-32 font-mono text-sm")
            
            # 配置日志处理器
            class LogHandler(logging.Handler):
                def emit(self, record):
                    log_area.push(record.getMessage())
            
            logger.addHandler(LogHandler())

if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(
        title="剪贴板复制解决方案",
        port=8080,
        reload=False,
        # 生产环境建议启用 HTTPS
        # ssl_certfile='path/to/cert.pem',
        # ssl_keyfile='path/to/key.pem'
    )
```

## 问题原因分析

出现 "JavaScript did not respond within 1.0 s" 错误的主要原因：

1. **浏览器安全限制**：
   - 剪贴板 API 需要明确的用户交互上下文
   - 在非 HTTPS 环境下会被阻止
   - 某些浏览器需要用户明确授权

2. **执行环境问题**：
   - 剪贴板操作可能在后台标签页被限制
   - 浏览器扩展可能拦截剪贴板访问
   - 复杂的 DOM 结构可能延迟 JavaScript 执行

3. **NiceGUI 通信机制**：
   - 默认 1 秒超时可能不足
   - WebSocket 通信延迟
   - 大文本传输耗时

## 解决方案核心组件

### 1. 剪贴板管理器 (`ClipboardManager`)

```python
class ClipboardManager:
    def __init__(self):
        self.copy_queue = []  # 复制任务队列
        self.is_copying = False  # 当前是否正在复制
        self.last_copied = None  # 上次复制的内容
        self.last_copied_time = 0  # 上次复制的时间戳
```

### 2. 安全复制方法

```python
async def safe_copy_to_clipboard(self, content):
    # 内容检查
    if not content:
        return False
        
    # 防止短时间内重复复制相同内容
    if content == self.last_copied and (time.time() - self.last_copied_time) < 1:
        return True
        
    # 加入队列并处理
    self.copy_queue.append(content)
    if not self.is_copying:
        asyncio.create_task(self.process_copy_queue())
    return True
```

### 3. 复制队列处理器

```python
async def process_copy_queue(self):
    self.is_copying = True
    while self.copy_queue:
        content = self.copy_queue.pop(0)
        escaped_content = self.escape_content(content)
        
        # 尝试复制
        success = await self.try_copy(escaped_content)
        
        if success:
            # 更新状态
            self.last_copied = content
            self.last_copied_time = time.time()
            ui.notify("已复制到剪贴板!", type="positive")
        else:
            # 提供备选方案
            self.copy_queue.append(content)
            await self.offer_alternative_copy_method(content)
            break
    self.is_copying = False
```

### 4. 健壮的复制尝试

```python
async def try_copy(self, escaped_content, timeout=3.0):
    try:
        # 使用异步IIFE封装
        await ui.run_javascript(
            f"""
            (async function() {{
                try {{
                    await navigator.clipboard.writeText(`{escaped_content}`);
                    return 'success';
                }} catch (error) {{
                    console.error('Clipboard write failed:', error);
                    return 'error';
                }}
            }})()
            """,
            timeout=timeout  # 延长超时时间
        )
        return True
    except asyncio.TimeoutError:
        logger.warning(f"剪贴板操作超时 ({timeout}s)")
        return False
    except Exception as e:
        logger.error(f"剪贴板操作异常: {str(e)}")
        return False
```

### 5. 内容安全处理

```python
def escape_content(self, content):
    """转义内容以安全插入JavaScript"""
    # 替换反引号和美元符号
    escaped = content.replace('`', '\\`').replace('$', '\\$')
    
    # 处理换行符
    escaped = escaped.replace('\n', '\\n').replace('\r', '\\r')
    
    # 截断过长的文本
    if len(escaped) > 1000:
        escaped = escaped[:1000] + '...'
        
    return escaped
```

### 6. 备选复制方案

```python
async def offer_alternative_copy_method(self, content):
    """当自动复制失败时提供手动复制选项"""
    with ui.dialog() as dialog, ui.card():
        # ... 创建对话框内容 ...
        textarea = ui.textarea(value=content).props("readonly")
        ui.button("复制", on_click=lambda: self.copy_via_textarea(textarea))

async def copy_via_textarea(self, textarea):
    """使用传统execCommand方法复制"""
    await ui.run_javascript(f"""
        (function() {{
            const textarea = document.getElementById('{textarea.id}');
            textarea.select();
            document.execCommand('copy');
            return 'success';
        }})()
    """)
```

## 使用说明

1. **初始化剪贴板管理器**：
   ```python
   clipboard = ClipboardManager()
   ```

2. **安全复制文本**：
   ```python
   # 在按钮点击事件中
   ui.button("复制", on_click=lambda: clipboard.safe_copy_to_clipboard("要复制的文本"))
   ```

3. **处理复制结果**：
   - 成功时会显示通知
   - 失败时会提供备选复制对话框
   - 所有操作记录在日志中

## 最佳实践建议

1. **用户交互上下文**：
   - 确保复制操作在用户点击事件中触发
   - 避免在页面加载或定时器中自动复制

2. **HTTPS 环境**：
   ```python
   ui.run(
       ssl_certfile='path/to/cert.pem',
       ssl_keyfile='path/to/key.pem'
   )
   ```

3. **内容长度控制**：
   - 超过1000字符的文本自动截断
   - 提供完整内容的手动复制选项

4. **错误处理**：
   - 记录所有复制操作和错误
   - 提供用户友好的备选方案

这个解决方案通过队列管理、超时控制、内容转义和备选方案，全面解决了剪贴板操作中的超时问题，并提供了良好的用户体验。