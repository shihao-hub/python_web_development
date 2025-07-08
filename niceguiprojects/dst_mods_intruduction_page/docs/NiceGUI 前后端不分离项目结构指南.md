# NiceGUI 前后端不分离项目结构指南

在 NiceGUI 中构建前后端不分离的项目，需要精心组织项目结构以确保代码可维护性和可扩展性。以下是一个完整的前后端不分离项目结构示例：

## 项目目录结构

```
my_nicegui_app/
├── app.py                  # 主应用入口
├── config.py               # 应用配置
├── requirements.txt        # 依赖列表
├── static/                 # 静态资源
│   ├── styles.css          # 全局样式
│   └── images/             # 图片资源
│       └── logo.png
├── templates/              # HTML模板（可选）
│   └── base.html
├── modules/                # 应用模块
│   ├── __init__.py
│   ├── auth.py             # 认证模块
│   ├── dashboard.py        # 仪表盘模块
│   ├── data_manager.py     # 数据管理模块
│   └── settings.py         # 设置模块
├── components/             # 可复用UI组件
│   ├── __init__.py
│   ├── header.py           # 页面头部组件
│   ├── sidebar.py          # 侧边栏组件
│   ├── card.py             # 卡片组件
│   └── form.py             # 表单组件
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── user.py             # 用户模型
│   └── data.py             # 数据模型
├── services/               # 业务逻辑服务
│   ├── __init__.py
│   ├── auth_service.py     # 认证服务
│   ├── data_service.py     # 数据处理服务
│   └── report_service.py   # 报表服务
└── utils/                  # 工具类
    ├── __init__.py
    ├── database.py         # 数据库工具
    ├── validators.py       # 验证工具
    └── helpers.py          # 辅助函数
```

## 详细说明

### 1. 主应用入口 (app.py)

```python
from nicegui import ui
from modules import auth, dashboard, data_manager, settings
from components import header, sidebar
from config import APP_CONFIG
import utils.database as db

# 初始化应用
def init_app():
    # 初始化数据库
    db.init_database(APP_CONFIG["DATABASE_URL"])
    
    # 加载全局样式
    ui.add_head_html('<link rel="stylesheet" href="/static/styles.css">')
    
    # 设置应用主题
    ui.dark_mode().enable()
    
    # 注册路由
    init_routes()

def init_routes():
    # 认证路由
    @ui.page('/login')
    def login_page():
        auth.render_login()
    
    @ui.page('/register')
    def register_page():
        auth.render_register()
    
    # 主应用路由
    @ui.page('/')
    def main_page():
        if not auth.is_authenticated():
            return ui.open('/login')
        
        with ui.header().classes('bg-blue-800 text-white p-4 shadow-md'):
            header.render()
        
        with ui.row().classes('w-full h-[calc(100vh-64px)]'):
            with ui.column().classes('w-64 bg-gray-100 h-full p-4 shadow-inner'):
                sidebar.render()
            
            with ui.column().classes('flex-grow p-6 overflow-auto'):
                ui.query('body').classes('bg-gray-50')
                dashboard.render()
    
    @ui.page('/data')
    def data_page():
        if not auth.is_authenticated():
            return ui.open('/login')
        
        with ui.header().classes('bg-blue-800 text-white p-4 shadow-md'):
            header.render()
        
        with ui.row().classes('w-full h-[calc(100vh-64px)]'):
            with ui.column().classes('w-64 bg-gray-100 h-full p-4 shadow-inner'):
                sidebar.render()
            
            with ui.column().classes('flex-grow p-6 overflow-auto'):
                data_manager.render()
    
    @ui.page('/settings')
    def settings_page():
        if not auth.is_authenticated():
            return ui.open('/login')
        
        with ui.header().classes('bg-blue-800 text-white p-4 shadow-md'):
            header.render()
        
        with ui.row().classes('w-full h-[calc(100vh-64px)]'):
            with ui.column().classes('w-64 bg-gray-100 h-full p-4 shadow-inner'):
                sidebar.render()
            
            with ui.column().classes('flex-grow p-6 overflow-auto'):
                settings.render()

if __name__ in {"__main__", "__mp_main__"}:
    init_app()
    ui.run(
        title="NiceGUI 全栈应用",
        port=8000,
        reload=APP_CONFIG["DEBUG"],
        favicon="static/images/logo.png",
        storage_secret=APP_CONFIG["SECRET_KEY"]
    )
```

### 2. 配置模块 (config.py)

```python
import os

class Config:
    # 基础配置
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    
    # 应用配置
    APP_NAME = "NiceGUI 全栈应用"
    VERSION = "1.0.0"
    
    # 认证配置
    SESSION_TIMEOUT = 3600  # 1小时
    
    # API配置
    API_PREFIX = "/api/v1"

# 导出配置对象
APP_CONFIG = {
    "DEBUG": Config.DEBUG,
    "SECRET_KEY": Config.SECRET_KEY,
    "DATABASE_URL": Config.DATABASE_URL,
    "APP_NAME": Config.APP_NAME,
    "VERSION": Config.VERSION,
    "SESSION_TIMEOUT": Config.SESSION_TIMEOUT,
    "API_PREFIX": Config.API_PREFIX
}
```

### 3. 认证模块 (modules/auth.py)

```python
from nicegui import ui
from models.user import User
from services.auth_service import authenticate_user, register_user
from utils.validators import validate_email, validate_password

def is_authenticated():
    """检查用户是否已认证"""
    return ui.storage.user.get('authenticated', False)

def render_login():
    """渲染登录页面"""
    ui.query('body').classes('bg-gray-100')
    
    with ui.card().classes('absolute-center p-8 w-full max-w-md'):
        ui.label('用户登录').classes('text-2xl font-bold mb-6 text-center')
        
        email = ui.input('邮箱').classes('w-full mb-4')
        password = ui.input('密码', password=True, password_toggle_button=True).classes('w-full mb-6')
        
        with ui.row().classes('w-full justify-between'):
            ui.button('登录', on_click=lambda: handle_login(email.value, password.value))
            ui.button('注册', on_click=lambda: ui.open('/register'))
        
        ui.link('忘记密码?', '/reset-password').classes('mt-4 text-sm text-blue-600')

def handle_login(email, password):
    """处理登录逻辑"""
    if not validate_email(email):
        ui.notify('请输入有效的邮箱地址', type='negative')
        return
    
    if not validate_password(password):
        ui.notify('密码长度至少为6个字符', type='negative')
        return
    
    user = authenticate_user(email, password)
    if user:
        # 存储用户会话
        ui.storage.user.update({
            'authenticated': True,
            'user_id': user.id,
            'email': user.email,
            'name': user.name
        })
        ui.open('/')
    else:
        ui.notify('邮箱或密码不正确', type='negative')

def render_register():
    """渲染注册页面"""
    ui.query('body').classes('bg-gray-100')
    
    with ui.card().classes('absolute-center p-8 w-full max-w-md'):
        ui.label('用户注册').classes('text-2xl font-bold mb-6 text-center')
        
        name = ui.input('姓名').classes('w-full mb-4')
        email = ui.input('邮箱').classes('w-full mb-4')
        password = ui.input('密码', password=True, password_toggle_button=True).classes('w-full mb-4')
        confirm_password = ui.input('确认密码', password=True, password_toggle_button=True).classes('w-full mb-6')
        
        ui.button('注册', on_click=lambda: handle_register(
            name.value, email.value, password.value, confirm_password.value
        ))
        
        ui.link('已有账号? 立即登录', '/login').classes('mt-4 text-sm text-blue-600')

def handle_register(name, email, password, confirm_password):
    """处理注册逻辑"""
    if not name:
        ui.notify('请输入姓名', type='negative')
        return
    
    if not validate_email(email):
        ui.notify('请输入有效的邮箱地址', type='negative')
        return
    
    if password != confirm_password:
        ui.notify('两次输入的密码不一致', type='negative')
        return
    
    if not validate_password(password):
        ui.notify('密码长度至少为6个字符', type='negative')
        return
    
    success, message = register_user(name, email, password)
    if success:
        ui.notify('注册成功! 请登录', type='positive')
        ui.open('/login')
    else:
        ui.notify(f'注册失败: {message}', type='negative')
```

### 4. 可复用组件 (components/header.py)

```python
from nicegui import ui
from utils import helpers

def render():
    """渲染应用头部"""
    with ui.row().classes('w-full justify-between items-center'):
        # 应用标题
        with ui.row().classes('items-center gap-3'):
            ui.icon('rocket', size='lg', color='white')
            ui.label('NiceGUI 应用').classes('text-xl font-bold')
        
        # 搜索框
        with ui.row().classes('flex-grow max-w-md mx-8'):
            search_input = ui.input(placeholder='搜索...').props('rounded outlined dense').classes('w-full')
            ui.button(icon='search', on_click=lambda: search(search_input.value))
        
        # 用户信息
        if helpers.is_authenticated():
            user_info = helpers.get_current_user()
            with ui.row().classes('items-center gap-3'):
                ui.icon('person', size='lg', color='white')
                ui.label(user_info['name']).classes('font-medium')
                with ui.menu().classes('bg-white') as menu:
                    ui.menu_item('个人资料', lambda: ui.open('/profile'))
                    ui.menu_item('设置', lambda: ui.open('/settings'))
                    ui.separator()
                    ui.menu_item('退出登录', logout)
                ui.button(icon='menu', on_click=menu.open).props('flat round dense')
        else:
            ui.button('登录', on_click=lambda: ui.open('/login')).props('outline')

def search(query):
    """处理搜索功能"""
    if query:
        ui.notify(f'搜索: {query}')
        # 实际应用中这里会执行搜索逻辑

def logout():
    """处理退出登录"""
    ui.storage.user.clear()
    ui.open('/login')
    ui.notify('您已成功退出登录', type='positive')
```

### 5. 数据模型 (models/user.py)

```python
from datetime import datetime
from utils.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import hashlib

class User(Base):
    """用户模型"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """设置密码哈希值"""
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        """验证密码"""
        return self.hashed_password == hashlib.sha256(password.encode()).hexdigest()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

### 6. 服务层 (services/auth_service.py)

```python
from sqlalchemy.orm import Session
from utils.database import get_db
from models.user import User

def authenticate_user(email: str, password: str) -> User:
    """认证用户"""
    with get_db() as db:
        user = db.query(User).filter(User.email == email).first()
        if user and user.check_password(password) and user.is_active:
            return user
    return None

def register_user(name: str, email: str, password: str) -> (bool, str):
    """注册新用户"""
    with get_db() as db:
        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == email).first():
            return False, "该邮箱已被注册"
        
        # 创建新用户
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        db.add(new_user)
        db.commit()
        
        return True, "注册成功"
    
    return False, "注册过程中发生错误"
```

### 7. 工具类 (utils/database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import APP_CONFIG

# 数据库配置
DATABASE_URL = APP_CONFIG["DATABASE_URL"]
Base = declarative_base()

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 项目结构设计原则

1. **分层架构**：
   - 表示层（UI）：`app.py`, `modules/`, `components/`
   - 业务逻辑层：`services/`
   - 数据访问层：`models/`
   - 工具层：`utils/`

2. **模块化设计**：
   - 按功能划分模块（认证、仪表盘、数据管理等）
   - 可复用UI组件单独存放
   - 服务类封装业务逻辑

3. **前后端融合**：
   - UI 逻辑与业务逻辑在同一个代码库
   - 使用 NiceGUI 的响应式设计处理前端交互
   - 直接在UI事件中调用业务逻辑

4. **状态管理**：
   - 使用 `ui.storage` 管理会话状态
   - 全局状态存储在服务层
   - 避免在UI组件中直接处理复杂业务逻辑

5. **配置管理**：
   - 集中管理应用配置
   - 支持环境变量覆盖
   - 类型安全的配置访问

## 开发建议

1. **代码组织**：
   - 保持每个文件只做一件事
   - 模块间通过明确定义的接口通信
   - 避免在UI组件中直接操作数据库

2. **性能优化**：
   - 使用分页加载大数据集
   - 实现缓存机制
   - 避免在UI线程执行耗时操作

3. **安全性**：
   - 对所有输入进行验证
   - 使用参数化查询防止SQL注入
   - 密码使用哈希存储

4. **测试策略**：
   - 为服务层编写单元测试
   - 为UI组件编写集成测试
   - 使用Mock对象隔离测试

5. **部署方案**：
   - 使用Gunicorn + Uvicorn部署
   - 配置Nginx反向代理
   - 启用HTTPS

## 优势与挑战

### 优势：
1. 开发效率高 - 前后端使用同一语言和技术栈
2. 部署简单 - 单一应用部署
3. 状态管理容易 - 无需处理跨域问题
4. 学习曲线平缓 - 只需掌握Python和NiceGUI

### 挑战：
1. 前端灵活性有限 - 受限于NiceGUI组件
2. 不适合大规模团队协作 - 前后端职责不清
3. 性能瓶颈 - 所有请求都在Python运行时处理
4. SEO支持有限 - 动态生成内容不易被搜索引擎索引

这种项目结构特别适合中小型应用、内部工具、原型开发等场景，能够快速构建功能完整的全栈应用。