# 使用 Django 实现反向代理方案

下面是一个完整的 Django 反向代理实现，将访问 `127.0.0.1:8888` 的请求透明地代理到运行在 `127.0.0.1:13000` 的服务：

## 完整实现代码

### 1. 创建 Django 项目和应用

```bash
# 创建项目目录
mkdir django_reverse_proxy
cd django_reverse_proxy

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 安装依赖
pip install django requests httpx

# 创建Django项目
django-admin startproject proxy_project .
django-admin startapp reverse_proxy
```

### 2. 配置代理视图

**文件: `reverse_proxy/views.py`**

```python
import httpx
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from urllib.parse import urljoin

# 目标服务地址
TARGET_SERVICE = "http://127.0.0.1:13000"

@method_decorator(csrf_exempt, name='dispatch')
class ReverseProxyView(View):
    """
    反向代理视图，处理所有请求并转发到目标服务
    """
    async def dispatch(self, request, path=""):
        # 构建目标URL
        target_url = urljoin(TARGET_SERVICE, request.get_full_path())
        
        # 准备请求头
        headers = self.prepare_headers(request)
        
        # 准备请求体
        content = await self.prepare_content(request)
        
        # 使用HTTPX发送异步请求
        async with httpx.AsyncClient() as client:
            # 发送请求到目标服务
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=content,
                cookies=request.COOKIES,
                allow_redirects=False,
                timeout=30.0
            )
            
            # 处理响应
            return self.handle_response(response)

    def prepare_headers(self, request):
        """准备要转发的请求头"""
        # 需要排除的请求头
        excluded_headers = {
            'host', 'content-length', 'connection', 
            'accept-encoding', 'accept-language'
        }
        
        # 构建新的请求头
        headers = {}
        for key, value in request.headers.items():
            # 转换头名称为标准格式 (e.g. HTTP_X_FORWARDED_FOR -> X-Forwarded-For)
            normalized_key = key.replace('HTTP_', '').replace('_', '-').title()
            
            # 跳过排除的头
            if normalized_key.lower() in excluded_headers:
                continue
            
            headers[normalized_key] = value
        
        # 添加X-Forwarded头
        headers['X-Forwarded-For'] = request.META.get('REMOTE_ADDR', '')
        headers['X-Forwarded-Host'] = request.get_host()
        headers['X-Forwarded-Proto'] = 'https' if request.is_secure() else 'http'
        
        return headers
    
    async def prepare_content(self, request):
        """准备请求体内容"""
        if request.method in ['GET', 'HEAD']:
            return None
        
        # 对于文件上传等大文件，使用流式读取
        if request.content_type == 'multipart/form-data':
            return request.body
        
        # 对于其他类型，读取整个body
        return await request.body
    
    def handle_response(self, response):
        """处理目标服务的响应"""
        # 创建流式响应
        proxy_response = StreamingHttpResponse(
            response.aiter_bytes(),
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/octet-stream')
        )
        
        # 复制响应头
        excluded_headers = {
            'content-encoding', 'content-length', 
            'transfer-encoding', 'connection'
        }
        
        for key, value in response.headers.items():
            if key.lower() in excluded_headers:
                continue
            proxy_response[key] = value
        
        # 设置内容长度（如果需要）
        if 'Content-Length' in response.headers:
            proxy_response['Content-Length'] = response.headers['Content-Length']
        
        return proxy_response
```

### 3. 配置 URL 路由

**文件: `reverse_proxy/urls.py`**

```python
from django.urls import path, re_path
from .views import ReverseProxyView

urlpatterns = [
    # 捕获所有路径并转发
    re_path(r'^(?P<path>.*)$', ReverseProxyView.as_view()),
]
```

**文件: `proxy_project/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 包含反向代理应用的URL
    path('', include('reverse_proxy.urls')),
]
```

### 4. 配置 Django 设置

**文件: `proxy_project/settings.py`**

```python
# 添加应用到INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reverse_proxy',  # 添加反向代理应用
]

# 中间件配置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 禁用CSRF保护（因为代理需要处理所有请求）
CSRF_TRUSTED_ORIGINS = ['http://localhost:8888', 'http://127.0.0.1:8888']
CSRF_COOKIE_SECURE = False  # 开发环境下禁用安全cookie

# 静态文件配置（可选）
STATIC_URL = '/static/'

# 配置日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### 5. 添加性能优化中间件

**文件: `reverse_proxy/middleware.py`**

```python
import time
from django.utils.deprecation import MiddlewareMixin

class ProxyPerformanceMiddleware(MiddlewareMixin):
    """代理性能监控中间件"""
    
    def process_request(self, request):
        request.start_time = time.time()
        return None
    
    def process_response(self, request, response):
        # 计算请求处理时间
        duration = (time.time() - request.start_time) * 1000
        
        # 添加X-Response-Time头
        response['X-Response-Time'] = f'{duration:.2f}ms'
        
        # 记录日志
        print(f"{request.method} {request.path} - {response.status_code} - {duration:.2f}ms")
        return response
```

**更新设置文件添加中间件:**

```python
# proxy_project/settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reverse_proxy.middleware.ProxyPerformanceMiddleware',  # 添加性能监控
]
```

### 6. 添加管理命令启动目标服务（可选）

**文件: `reverse_proxy/management/commands/run_target.py`**

```python
from django.core.management.base import BaseCommand
import subprocess
import os

class Command(BaseCommand):
    help = '启动目标服务（端口13000）'
    
    def handle(self, *args, **options):
        # 这里假设目标服务是一个简单的HTTP服务器
        # 在实际应用中，您应该替换为启动您实际服务的命令
        self.stdout.write(self.style.SUCCESS('启动目标服务...'))
        
        # 示例：启动一个简单的Python HTTP服务器
        try:
            # 注意：这只是一个示例，实际应用中应替换为您的服务启动命令
            subprocess.run(
                ["python", "-m", "http.server", "13000", "--directory", os.getcwd()],
                check=True
            )
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('目标服务已停止'))
```

## 运行反向代理

### 1. 启动目标服务（端口13000）

```bash
# 启动一个简单的HTTP服务器作为目标服务
python -m http.server 13000 --directory /path/to/your/content
```

### 2. 启动Django反向代理（端口8888）

```bash
# 迁移数据库（如果需要）
python manage.py migrate

# 启动Django开发服务器
python manage.py runserver 8888
```

### 3. 测试代理功能

访问 `http://127.0.0.1:8888`，您将看到运行在 `127.0.0.1:13000` 的服务内容。

## 高级功能扩展

### 1. 添加基本认证

```python
# reverse_proxy/views.py
from django.contrib.auth import authenticate
from django.http import HttpResponse

class ReverseProxyView(View):
    async def dispatch(self, request, path=""):
        # 检查基本认证
        if not self.check_basic_auth(request):
            return self.require_auth()
        
        # ...其余代码不变...
    
    def check_basic_auth(self, request):
        """检查基本认证"""
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Basic '):
            return False
        
        # 解码凭据
        import base64
        try:
            credentials = base64.b64decode(auth[6:]).decode('utf-8')
            username, password = credentials.split(':', 1)
        except:
            return False
        
        # 验证凭据（在实际应用中应从数据库验证）
        return username == 'admin' and password == 'secret'
    
    def require_auth(self):
        """返回认证要求响应"""
        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Restricted Area"'
        return response
```

### 2. 添加请求缓存

```python
# reverse_proxy/views.py
from django.core.cache import cache

class ReverseProxyView(View):
    async def dispatch(self, request, path=""):
        # 检查缓存
        cache_key = self.get_cache_key(request)
        cached_response = cache.get(cache_key)
        
        if cached_response:
            return self.build_cached_response(cached_response)
        
        # 处理请求...
        response = await self.proxy_request(request)
        
        # 缓存响应（仅GET请求且状态为200）
        if request.method == 'GET' and response.status_code == 200:
            cache.set(cache_key, {
                'status': response.status_code,
                'headers': dict(response.headers),
                'content': b''.join([chunk async for chunk in response.aiter_bytes()]),
                'content_type': response.headers.get('Content-Type')
            }, timeout=300)  # 缓存5分钟
        
        return response
    
    def get_cache_key(self, request):
        """生成缓存键"""
        return f"proxy_cache:{request.get_full_path()}"
    
    def build_cached_response(self, cached_data):
        """从缓存数据构建响应"""
        response = HttpResponse(
            cached_data['content'],
            status=cached_data['status'],
            content_type=cached_data['content_type']
        )
        for key, value in cached_data['headers'].items():
            response[key] = value
        response['X-Cache'] = 'HIT'
        return response
```

### 3. 添加请求过滤

```python
# reverse_proxy/views.py
class ReverseProxyView(View):
    async def dispatch(self, request, path=""):
        # 检查请求是否允许
        if not self.is_request_allowed(request):
            return HttpResponseForbidden("Access to this resource is restricted")
        
        # ...其余代码不变...
    
    def is_request_allowed(self, request):
        """检查请求是否允许"""
        # 阻止特定路径
        if request.path.startswith('/admin/'):
            return False
        
        # 阻止特定方法
        if request.method in ['DELETE', 'PUT']:
            return False
        
        # 阻止特定用户代理
        user_agent = request.headers.get('User-Agent', '').lower()
        if 'curl' in user_agent or 'wget' in user_agent:
            return False
        
        return True
```

### 4. 添加速率限制

```python
# reverse_proxy/views.py
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests

class ReverseProxyView(View):
    RATE_LIMIT = 100  # 每分钟最多100个请求
    
    async def dispatch(self, request, path=""):
        # 检查速率限制
        client_ip = self.get_client_ip(request)
        if not self.check_rate_limit(client_ip):
            return HttpResponseTooManyRequests("Rate limit exceeded")
        
        # ...其余代码不变...
    
    def get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, client_ip):
        """检查速率限制"""
        cache_key = f"rate_limit:{client_ip}"
        request_count = cache.get(cache_key, 0)
        
        if request_count >= self.RATE_LIMIT:
            return False
        
        cache.set(cache_key, request_count + 1, timeout=60)
        return True
```

## 生产环境部署建议

### 1. 使用 ASGI 服务器

```bash
pip install uvicorn

# 启动Uvicorn服务器
uvicorn proxy_project.asgi:application --port 8888
```

### 2. 添加 Gunicorn 作为 WSGI 服务器

```bash
pip install gunicorn

# 启动Gunicorn服务器
gunicorn proxy_project.wsgi:application -b 0.0.0.0:8888 -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. 配置 NGINX 作为前端代理

**文件: `/etc/nginx/sites-available/django_proxy`**

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 静态文件直接由Nginx处理
    location /static/ {
        alias /path/to/your/project/static/;
        expires 30d;
    }
}
```

### 4. 添加 SSL/TLS 支持

使用 Let's Encrypt 获取免费 SSL 证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 性能优化技巧

1. **连接池优化**:
   ```python
   # reverse_proxy/views.py
   import httpx
   
   # 创建全局连接池
   client = httpx.AsyncClient(
       limits=httpx.Limits(
           max_connections=100,
           max_keepalive_connections=20,
           keepalive_expiry=30
       ),
       timeout=30.0
   )
   
   class ReverseProxyView(View):
       async def dispatch(self, request, path=""):
           # 使用全局client代替每次创建新client
           response = await client.request(...)
   ```

2. **响应压缩**:
   ```python
   # reverse_proxy/middleware.py
   import gzip
   from io import BytesIO
   
   class CompressionMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response
           
       def __call__(self, request):
           response = self.get_response(request)
           
           # 检查客户端是否支持gzip
           if 'gzip' in request.headers.get('Accept-Encoding', '') and \
              response.status_code == 200 and \
              response.get('Content-Encoding', None) is None:
               
               # 压缩内容
               content = b''.join(response.streaming_content)
               buffer = BytesIO()
               with gzip.GzipFile(fileobj=buffer, mode='wb') as gzip_file:
                   gzip_file.write(content)
               
               response.content = buffer.getvalue()
               response['Content-Encoding'] = 'gzip'
               response['Content-Length'] = str(len(response.content))
           
           return response
   ```

3. **静态文件缓存**:
   ```python
   # reverse_proxy/views.py
   from django.conf import settings
   from django.views.static import serve
   
   class ReverseProxyView(View):
       async def dispatch(self, request, path=""):
           # 如果是静态文件，直接由Django处理
           if path.startswith(settings.STATIC_URL):
               return serve(request, path, document_root=settings.STATIC_ROOT)
           
           # 否则代理请求
           return await self.proxy_request(request)
   ```

## 安全注意事项

1. **请求头过滤**:
   ```python
   # reverse_proxy/views.py
   class ReverseProxyView(View):
       def prepare_headers(self, request):
           # ...
           # 过滤敏感头
           sensitive_headers = ['authorization', 'cookie', 'set-cookie']
           for key in list(headers.keys()):
               if key.lower() in sensitive_headers:
                   del headers[key]
           # ...
   ```

2. **防止 HTTP 头注入**:
   ```python
   class ReverseProxyView(View):
       def handle_response(self, response):
           # ...
           # 验证响应头
           valid_headers = []
           for key, value in response.headers.items():
               if '\n' in key or '\r' in key or '\n' in value or '\r' in value:
                   continue  # 跳过包含换行符的潜在危险头
               valid_headers.append((key, value))
           # ...
   ```

3. **请求大小限制**:
   ```python
   # proxy_project/settings.py
   DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
   FILE_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20MB
   ```

## 完整项目结构

```
django_reverse_proxy/
├── venv/                   # 虚拟环境
├── proxy_project/          # Django项目
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # 项目设置
│   ├── urls.py             # 主URL配置
│   └── wsgi.py
├── reverse_proxy/          # 代理应用
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── middleware.py       # 自定义中间件
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py             # 应用URL配置
│   └── views.py            # 代理视图
├── manage.py
└── requirements.txt        # 依赖列表
```

## 总结

这个 Django 反向代理方案提供了以下功能：

1. **完全透明的代理**：将 8888 端口的请求无缝转发到 13000 端口
2. **高性能异步处理**：使用 HTTPX 和异步视图提高并发性能
3. **完整的 HTTP 支持**：处理所有 HTTP 方法、请求头和响应头
4. **安全防护**：包含基本认证、请求过滤和速率限制
5. **性能优化**：支持缓存、压缩和连接池
6. **生产就绪**：提供 ASGI/Uvicorn 和 Nginx 部署方案

要使用此代理：
1. 启动目标服务在 13000 端口
2. 启动 Django 代理在 8888 端口
3. 访问 `http://127.0.0.1:8888` 即可看到目标服务内容

此方案特别适合：
- 开发环境中的跨端口访问
- 本地服务的集成测试
- 为无域名的服务提供代理访问
- 在现有 Django 项目中集成外部服务