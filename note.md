## NiceGUI
### 组件大全
- ui.switch：开关
- ui.lable：显示一些文本
```python
# 重写 _handle_text_change 方法，根据标签的内容来更新其其他属性

from nicegui import ui


class status_label(ui.label):
    def _handle_text_change(self, text: str) -> None:
        super()._handle_text_change(text)
        if text == 'ok':
            self.classes(replace='text-positive')
        else:
            self.classes(replace='text-negative')


model = {'status': 'error'}
status_label().bind_text_from(model, 'status')
ui.switch(on_change=lambda e: model.update(status='ok' if e.value else 'error'))

ui.run()
```
- ui.link: 创建超链接
...（详情参见：https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/index.html 自己记笔记不如多看笔记）

### Others

important:
- 折线图：https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/data/line-plot.html
- Matplotlib 绘图：
- Plotly 图表：
- 线性进度条：
- 3D 场景：
- ECharts 图表：
- Highcharts 图表：
- Leaflet 地图：
- 表格：
- AG Grid：



## Undefined Notes


---

将 https://visionz.readthedocs.io/zh-cn/latest/ext/nicegui/index.html 中的
所有控件汇总成：代码+图片 和 仅图片，仅图片功能有助于我们了解组件从而进行拼装开发。

---

nicegui 有 move 功能，可以将组件移动到其他组件里。这个能实现拖拽功能吗？


---

只在 apps 存放 fastapi 相关内容（nicegui 本就依赖于 fastapi），
除此以外，外面的目录涉及代码的，理当只和 nicegui 有关， 尽力减少与 fastapi 的关联。

理由：首先，fastapi 相关我用的应该不多，其次，nicegui 主要还是前端开发为主。

---

前端本就不是我的强项，所以尽量减少复杂度，不要搞什么模块化，直接放在一起，不要搞什么目录结构。

更别说 nicegui 本就轻量化，所以进行一次尝试：整个前端项目不要有目录结构，文件全部同级！


---

下面的结构仅供参考，nicegui 理当专注前端，后端涉及 fastapi 的内容不应该复杂化

```txt
frontend/
├── app/
│   ├── api/                  # FastAPI路由（API端点）
│   │   ├── routers/          # 拆分不同的路由模块
│   │   │   ├── items.py      # 示例：item相关路由
│   │   │   ├── users.py      # 用户相关路由
│   │   │   └── __init__.py
│   │   ├── dependencies.py   # 依赖注入（如认证等）
│   │   └── __init__.py       # 创建FastAPI路由总汇
│   ├── pages/                # NiceGUI页面
│   │   ├── home.py
│   │   ├── dashboard.py
│   │   └── ... 
│   ├── components/           # UI组件
│   │   └── ...
│   ├── static/               # 静态文件
│   ├── utils/                # 工具函数
│   ├── models/               # 数据模型（若需要）
│   │   ├── item.py
│   │   └── user.py
│   ├── services/             # 业务逻辑层（可选）
│   │   ├── item_service.py
│   │   └── user_service.py
│   ├── db/                   # 数据库相关
│   │   ├── database.py       # 数据库连接等
│   │   └── crud.py           # 数据库操作
│   ├── main.py               # 应用主入口
│   └── config.py             # 配置管理
├── tests/
│   ├── test_api/
│   ├── test_pages/
│   └── ...
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile                # 可选，用于容器化部署
└── README.md






my_nicegui_project/
├── app/                      # 主应用目录
│   ├── pages/                # 页面模块
│   │   ├── home.py           # 首页逻辑
│   │   ├── dashboard.py      # 仪表盘页面
│   │   ├── settings.py       # 设置页面
│   │   └── __init__.py       # 页面包初始化
│   ├── components/           # 可复用UI组件
│   │   ├── header.py         # 页面头部组件
│   │   ├── sidebar.py        # 侧边栏组件
│   │   ├── card.py           # 卡片组件
│   │   └── __init__.py       # 组件包初始化
│   ├── static/               # 静态资源
│   │   ├── styles/           # CSS样式
│   │   │   └── main.css      # 主样式表
│   │   ├── images/           # 图片资源
│   │   └── scripts/          # JavaScript文件
│   ├── utils/                # 工具函数
│   │   ├── auth.py           # 认证工具
│   │   ├── database.py       # 数据库连接
│   │   └── helpers.py        # 辅助函数
│   └── main.py               # 应用入口点
├── tests/                    # 测试目录
│   ├── test_components.py    # 组件测试
│   └── test_pages.py         # 页面测试
├── .env                      # 环境变量
├── .gitignore                # Git忽略规则
├── requirements.txt          # Python依赖
└── README.md                 # 项目文档






my-nicegui-project/
├── backend/                      # FastAPI 后端代码
│   ├── src/                      # 应用源代码
│   │   ├── api/                  # API 路由
│   │   │   ├── v1/               # API 版本控制
│   │   │   │   ├── endpoints/    # API端点模块
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── items.py
│   │   │   │   │   └── __init__.py
│   │   │   │   ├── routers.py    # API路由聚合
│   │   │   │   └── __init__.py
│   │   ├── core/                 # 核心功能
│   │   │   ├── config.py         # 配置管理
│   │   │   ├── security.py       # 认证和安全
│   │   │   ├── dependencies.py   # 依赖注入
│   │   │   └── __init__.py
│   │   ├── db/                   # 数据库相关
│   │   │   ├── session.py        # 数据库会话
│   │   │   ├── models.py         # SQLAlchemy 模型
│   │   │   ├── repositories/     # 数据访问层
│   │   │   │   ├── user_repo.py
│   │   │   │   └── item_repo.py
│   │   │   └── __init__.py
│   │   ├── schemas/              # Pydantic 模型
│   │   │   ├── user.py
│   │   │   ├── item.py
│   │   │   └── __init__.py
│   │   ├── services/             # 业务逻辑层
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   └── item_service.py
│   │   ├── utils/                # 工具函数
│   │   │   ├── logger.py
│   │   │   └── helpers.py
│   │   ├── main.py               # FastAPI 应用入口
│   │   └── __init__.py
│   ├── tests/                    # 测试代码
│   │   ├── api/
│   │   │   └── v1/
│   │   ├── conftest.py
│   │   └── __init__.py
│   ├── requirements.txt          # Python 依赖
│   ├── Dockerfile                # 后端 Dockerfile
│   └── alembic/                  # 数据库迁移
│       ├── versions/             # 迁移脚本
│       ├── env.py
│       └── script.py.mako
│
├── frontend/                     # NiceGUI 前端代码
│   ├── src/                      # 前端源代码
│   │   ├── assets/               # 静态资源
│   │   │   ├── css/              # 自定义样式
│   │   │   │   └── custom.css
│   │   │   ├── images/           # 图片资源
│   │   │   └── fonts/            # 字体文件
│   │   ├── components/           # 可复用UI组件
│   │   │   ├── layout/           # 布局组件
│   │   │   │   ├── header.py
│   │   │   │   ├── sidebar.py
│   │   │   │   └── footer.py
│   │   │   ├── ui/               # UI元素组件
│   │   │   │   ├── card.py
│   │   │   │   ├── table.py
│   │   │   │   └── form.py
│   │   │   └── __init__.py
│   │   ├── pages/                # 页面模块
│   │   │   ├── auth/             # 认证页面
│   │   │   │   ├── login.py
│   │   │   │   └── register.py
│   │   │   ├── dashboard.py      # 仪表盘
│   │   │   ├── users.py          # 用户管理
│   │   │   ├── items.py          # 项目管理
│   │   │   └── __init__.py
│   │   ├── services/             # 前端服务
│   │   │   ├── api_client.py     # API 客户端
│   │   │   ├── auth.py           # 认证状态管理
│   │   │   └── event_bus.py      # 事件总线
│   │   ├── stores/               # 状态管理
│   │   │   ├── user_store.py     # 用户状态
│   │   │   └── app_store.py      # 应用全局状态
│   │   ├── app.py                # NiceGUI 应用入口
│   │   └── __init__.py
│   ├── requirements.txt          # 前端依赖
│   ├── Dockerfile                # 前端 Dockerfile
│   └── .env                      # 前端环境变量
│
├── docker-compose.yml            # Docker 编排配置
├── .gitignore
├── README.md                     # 项目文档
├── pyproject.toml                # Python 项目配置
├── .env                          # 全局环境变量
└── scripts/                      # 实用脚本
    ├── setup_db.sh               # 数据库初始化脚本
    └── run_tests.sh              # 测试运行脚本

```

---


