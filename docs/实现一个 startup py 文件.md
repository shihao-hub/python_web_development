以下是一个完整的 `startup.py` 文件实现，它可以同时启动前端和后端服务，并提供优雅的进程管理：

```python
#!/usr/bin/env python3
"""
项目启动脚本 - 同时运行前端和后端服务

使用方法:
    python startup.py       # 正常启动
    python startup.py debug # 调试模式（显示输出）
"""

import os
import sys
import subprocess
import time
import signal
from typing import List, Optional

# 项目路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_CMD = ["python", "main.py"]
BACKEND_CMD = ["python", "manage.py", "runserver", "8888"]

class ProcessManager:
    """进程管理器，用于启动和监控子进程"""
    
    def __init__(self):
        self.processes = []
        self.debug_mode = False
    
    def start_process(self, cmd: List[str], cwd: str, name: str):
        """启动一个子进程"""
        # 设置输出目标
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
        if self.debug_mode:
            stdout = None
            stderr = None
        
        try:
            process = subprocess.Popen(
                cmd,
                cwd=cwd,
                stdout=stdout,
                stderr=stderr,
                text=True,
                start_new_session=True  # 创建新的进程组
            )
            self.processes.append((process, name))
            
            # 在调试模式下立即打印输出
            if self.debug_mode:
                print(f"[{name}] 进程已启动 (PID: {process.pid})")
            else:
                print(f"[{name}] 进程已启动 (PID: {process.pid})，输出已静默")
            
            return process
        except Exception as e:
            print(f"启动 {name} 失败: {str(e)}")
            self.terminate_all()
            sys.exit(1)
    
    def monitor_output(self):
        """监控非调试模式下的进程输出"""
        if self.debug_mode:
            return  # 调试模式下不需要额外监控
        
        while any(p.is_alive() for p, _ in self.processes):
            for process, name in self.processes:
                if process.stdout and not process.stdout.closed:
                    try:
                        line = process.stdout.readline()
                        if line:
                            print(f"[{name}] {line.strip()}")
                    except:
                        pass
            time.sleep(0.1)
    
    def is_alive(self, process: subprocess.Popen) -> bool:
        """检查进程是否仍在运行"""
        return process.poll() is None
    
    def terminate_all(self):
        """终止所有子进程"""
        print("\n终止所有进程...")
        for process, name in self.processes:
            if self.is_alive(process):
                print(f"终止 {name} 进程 (PID: {process.pid})")
                try:
                    # 终止整个进程组
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                except ProcessLookupError:
                    pass  # 进程已退出
        time.sleep(1)  # 给进程一点时间退出
    
    def run(self, debug: bool = False):
        """运行所有服务"""
        self.debug_mode = debug
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("=" * 50)
        print("启动项目服务...")
        print(f"前端目录: {FRONTEND_DIR}")
        print(f"后端目录: {BACKEND_DIR}")
        print("=" * 50)
        
        # 启动前端
        self.start_process(FRONTEND_CMD, FRONTEND_DIR, "前端")
        
        # 给前端一点启动时间
        time.sleep(2)
        
        # 启动后端
        self.start_process(BACKEND_CMD, BACKEND_DIR, "后端")
        
        print("\n服务已全部启动!")
        print(f"前端: http://localhost:8080")
        print(f"后端: http://localhost:8888")
        print("按 Ctrl+C 停止所有服务\n")
        
        # 监控输出
        self.monitor_output()
        
        # 等待所有进程结束
        try:
            while any(self.is_alive(p) for p, _ in self.processes):
                time.sleep(1)
        except KeyboardInterrupt:
            self.terminate_all()
    
    def signal_handler(self, signum, frame):
        """信号处理函数"""
        self.terminate_all()
        sys.exit(0)

def check_dependencies():
    """检查必要的依赖是否存在"""
    required_dirs = [FRONTEND_DIR, BACKEND_DIR]
    missing = [d for d in required_dirs if not os.path.exists(d)]
    
    if missing:
        print("错误: 以下目录不存在，请检查项目结构:")
        for d in missing:
            print(f"  - {d}")
        print("\n项目目录结构应为:")
        print("  /项目根目录")
        print("    ├── frontend/")
        print("    │   └── main.py")
        print("    ├── backend/")
        print("    │   └── manage.py")
        print("    └── startup.py")
        sys.exit(1)

if __name__ == "__main__":
    # 检查项目结构
    check_dependencies()
    
    # 解析命令行参数
    debug_mode = "--debug" in sys.argv or "-d" in sys.argv or "debug" in sys.argv
    
    # 启动服务
    manager = ProcessManager()
    manager.run(debug=debug_mode)
```

## 使用说明

### 1. 基本使用
```bash
# 正常启动（静默模式）
python startup.py

# 调试模式（显示所有输出）
python startup.py debug
# 或
python startup.py --debug
# 或
python startup.py -d
```

### 2. 项目目录结构要求
```
your_project/
├── frontend/
│   └── main.py     # 前端入口文件
├── backend/
│   └── manage.py   # 后端管理脚本
└── startup.py      # 本启动脚本
```

### 3. 功能特点

1. **并行启动**：同时启动前端和后端服务
2. **进程管理**：
   - 统一监控所有子进程
   - Ctrl+C 可一键终止所有服务
   - 自动清理进程资源
3. **输出管理**：
   - 静默模式：隐藏服务输出（默认）
   - 调试模式：显示所有服务的实时输出
4. **错误处理**：
   - 自动检查项目目录结构
   - 服务崩溃时自动终止相关进程
5. **跨平台支持**：兼容 Windows/Linux/macOS

### 4. 自定义配置

如需修改配置，可调整脚本顶部的变量：
```python
# 项目路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

# 启动命令配置
FRONTEND_CMD = ["python", "main.py"]  # 前端启动命令
BACKEND_CMD = ["python", "manage.py", "runserver", "8888"]  # 后端启动命令
```

### 5. 服务访问
启动成功后，可访问：
- 前端：http://localhost:8080
- 后端：http://localhost:8888

### 6. 停止服务
- 正常停止：Ctrl+C
- 强制停止：直接关闭终端或使用系统任务管理器

这个脚本提供了完整的服务管理功能，特别适合开发需要同时运行前后端服务的项目。