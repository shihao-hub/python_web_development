# Django 中间件（Middleware）添加指南

在 Django 中，中间件是处理请求和响应的轻量级插件系统，允许你在请求处理流程的不同阶段添加自定义功能。下面是添加和使用中间件的完整指南。

## 中间件的作用

中间件可以用于：
1. 请求预处理（如身份验证、日志记录）
2. 响应后处理（如添加头部信息、内容修改）
3. 异常处理
4. 视图函数执行前后的操作

## 创建自定义中间件

### 1. 创建中间件文件

在 Django 应用目录中创建 `middleware.py` 文件：

```python
# myapp/middleware.py
import time
from django.utils.deprecation import MiddlewareMixin

class SimpleTimingMiddleware(MiddlewareMixin):
    """计算请求处理时间的中间件"""
    
    def process_request(self, request):
        """在请求到达视图之前执行"""
        request.start_time = time.time()
    
    def process_response(self, request, response):
        """在响应返回给客户端之前执行"""
        duration = time.time() - request.start_time
        response["X-Response-Time"] = f"{duration:.2f}s"
        return response

class AuthMiddleware(MiddlewareMixin):
    """简单的身份验证中间件"""
    
    def process_request(self, request):
        """检查用户是否已认证"""
        if not request.user.is_authenticated and not request.path.startswith('/login/'):
            from django.shortcuts import redirect
            return redirect('/login/')
        return None
```

### 2. 注册中间件

在 `settings.py` 文件中添加自定义中间件：

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 添加自定义中间件
    'myapp.middleware.SimpleTimingMiddleware',
    'myapp.middleware.AuthMiddleware',
]
```

## 中间件执行顺序

Django 中间件的执行顺序很重要：

1. **请求阶段**：从上到下执行（`settings.MIDDLEWARE` 列表顺序）
2. **响应阶段**：从下到上执行（`settings.MIDDLEWARE` 列表逆序）

```
Request → Middleware1 → Middleware2 → View → Middleware2 → Middleware1 → Response
```

## 中间件方法详解

### 核心方法

| 方法名 | 描述 | 返回值 |
|--------|------|---------|
| `__init__(self, get_response)` | 初始化方法，只调用一次 | - |
| `__call__(self, request)` | 处理请求的主要方法 | 响应对象 |
| `process_request(self, request)` | 请求到达视图前执行 | `None` 或 `HttpResponse` |
| `process_view(self, request, view_func, view_args, view_kwargs)` | 在调用视图前执行 | `None` 或 `HttpResponse` |
| `process_template_response(self, request, response)` | 处理模板响应 | 响应对象 |
| `process_exception(self, request, exception)` | 处理视图异常 | `None` 或 `HttpResponse` |
| `process_response(self, request, response)` | 在响应返回客户端前执行 | 响应对象 |

### 使用示例

```python
# myapp/middleware.py
from django.http import HttpResponseForbidden

class IPRestrictionMiddleware(MiddlewareMixin):
    """IP限制中间件"""
    ALLOWED_IPS = ['127.0.0.1', '192.168.1.0/24']
    
    def process_request(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        
        # 检查IP是否允许
        if not any(client_ip.startswith(ip) for ip in self.ALLOWED_IPS):
            return HttpResponseForbidden("Access Denied")
        return None

class ContentSecurityPolicyMiddleware:
    """添加安全策略头部"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        response['Content-Security-Policy'] = "default-src 'self'"
        return response
```

## 高级中间件模式

### 1. 基于类的中间件（推荐）

```python
class CustomHeaderMiddleware:
    """添加自定义HTTP头部"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 请求处理前
        if 'X-Custom-Header' not in request.headers:
            request.custom_header = "Default Value"
        else:
            request.custom_header = request.headers['X-Custom-Header']
        
        response = self.get_response(request)
        
        # 响应处理后
        response['X-Custom-Response'] = "Processed"
        return response
```

### 2. 函数式中间件

```python
def simple_middleware(get_response):
    """函数式中间件示例"""
    # 一次性初始化代码
    print("Middleware initialized")
    
    def middleware(request):
        # 请求处理前
        print(f"Processing request: {request.path}")
        
        response = get_response(request)
        
        # 响应处理后
        print(f"Completed request: {request.path}")
        return response
    
    return middleware
```

## 常用内置中间件

| 中间件类 | 功能 |
|----------|------|
| `SecurityMiddleware` | 安全相关功能（HTTPS重定向等） |
| `SessionMiddleware` | 会话管理 |
| `CsrfViewMiddleware` | CSRF保护 |
| `AuthenticationMiddleware` | 用户认证 |
| `MessageMiddleware` | 消息传递 |
| `CommonMiddleware` | 常用功能（URL规范化等） |
| `GZipMiddleware` | 响应压缩 |
| `LocaleMiddleware` | 国际化支持 |

## 最佳实践

1. **保持中间件轻量**：避免在中间件中执行耗时操作
2. **注意执行顺序**：中间件顺序会影响功能
3. **合理使用异常处理**：使用 `process_exception` 处理错误
4. **避免循环依赖**：确保中间件不依赖未初始化的组件
5. **测试中间件**：编写测试确保中间件行为正确
6. **使用中间件名称**：为调试提供清晰标识

```python
# 测试中间件示例
from django.test import RequestFactory
from .middleware import SimpleTimingMiddleware

def test_timing_middleware():
    middleware = SimpleTimingMiddleware(lambda r: HttpResponse())
    request = RequestFactory().get('/')
    response = middleware(request)
    assert 'X-Response-Time' in response
```

## 常见问题解决

### 中间件不生效
1. 检查 `settings.py` 中的 `MIDDLEWARE` 列表是否包含你的中间件
2. 确保中间件路径正确（`app.middleware.ClassName`）
3. 验证中间件没有抛出未处理异常

### 循环导入问题
如果中间件依赖其他应用组件：
```python
class LateImportMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 避免在顶部导入
        from myapp.models import Config
        self.config = Config.load()
    
    def __call__(self, request):
        # 使用 self.config
        return self.get_response(request)
```

### 性能优化
对于频繁使用的中间件：
```python
class CachedMiddleware:
    _cache = {}
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 使用缓存避免重复计算
        if request.path in self._cache:
            return self._cache[request.path]
        
        response = self.get_response(request)
        self._cache[request.path] = response
        return response
```

## 实际应用场景

1. **请求日志记录**
```python
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        import logging
        self.logger = logging.getLogger('request')
    
    def __call__(self, request):
        self.logger.info(f"Incoming request: {request.method} {request.path}")
        response = self.get_response(request)
        self.logger.info(f"Response status: {response.status_code}")
        return response
```

2. **用户时区设置**
```python
class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            timezone = request.user.profile.timezone
            import pytz
            from django.utils import timezone as dj_timezone
            dj_timezone.activate(pytz.timezone(timezone))
        return self.get_response(request)
```

3. **API版本控制**
```python
class APIVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        version = request.headers.get('X-API-Version', 'v1')
        request.api_version = version
        response = self.get_response(request)
        response['X-API-Version'] = version
        return response
```

## 总结

Django 中间件提供了强大的请求/响应处理管道：
1. 创建中间件类或函数
2. 在 `settings.MIDDLEWARE` 中注册
3. 实现所需的方法（`process_request`, `process_response` 等）
4. 注意中间件执行顺序的重要性

正确使用中间件可以：
- 集中处理横切关注点（如认证、日志）
- 增强应用程序安全性
- 简化视图函数逻辑
- 实现全局功能而无需修改每个视图

遵循最佳实践并充分测试中间件，可以构建出更健壮、可维护的 Django 应用程序。
