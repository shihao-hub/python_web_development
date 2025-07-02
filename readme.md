### 启动服务

启动前端：`python ./frontend/main.py`

启动后端（开发环境）：`python ./backend/manager.py runserver 8888`

#### 前端项目服务器托管
参考链接：https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/deploy/ServerHosting.html

```txt
[install nicegui]
pip install nicegui

[start nicegui server]
使用 systemd 或类似的服务来启动主脚本（python main.py）

只需要上述操作就能做到 nicegui 项目部署（包括正式环境，不像 django 严格要求正式环境不要使用 runserver 命令）
```
