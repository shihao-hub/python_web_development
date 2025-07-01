在 Django 中，`HttpResponsePermanentRedirect`（HTTP 301 重定向）**不会自动携带原始请求的所有信息**，但可以通过特定方式传递某些信息。以下是关键细节：

### 1. **Cookie 和 Session 的传递**
- **Cookies**：
  - 浏览器会在重定向请求中**自动携带所有匹配目标域名的 Cookies**
  - 如果重定向前后域名相同（或父域匹配），浏览器会自动发送相关 Cookies（包括 sessionid）
  - 示例：
    ```python
    # 原始请求携带的 Cookie 会被发送到重定向目标（如果域名匹配）
    # 浏览器行为，非 Django 自动添加
    ```

- **Session**：
  - Session 依赖 `sessionid` Cookie
  - 如果 `sessionid` Cookie 在重定向后仍有效且域名匹配，Session 数据保持不变
  - Django 不会在重定向响应中自动创建新 Session

### 2. **HttpResponsePermanentRedirect 的特性**
```python
from django.http import HttpResponsePermanentRedirect

def my_view(request):
    # 不会自动携带请求数据
    return HttpResponsePermanentRedirect("/new-url/")
```

- ❌ **不携带**：
  - POST 请求体数据
  - 请求头（如 Authorization）
  - 查询参数（除非手动添加）
  - 非 Cookie 的请求状态

- ✅ **可通过以下方式传递**：
  ```python
  # 方法 1：通过 URL 参数传递数据
  return HttpResponsePermanentRedirect(f"/new-url/?token={token}")
  
  # 方法 2：设置 Cookie（显式）
  response = HttpResponsePermanentRedirect("/new-url/")
  response.set_cookie('data', value, domain=".example.com")
  return response
  
  # 方法 3：Session 存储（需 sessionid Cookie 有效）
  request.session['temp_data'] = data  # 存储到 session
  return HttpResponsePermanentRedirect("/new-url/")
  ```

### 3. 关键考虑因素
| 项目               | 是否自动携带               | 说明                                                                 |
|--------------------|----------------------------|----------------------------------------------------------------------|
| Cookies            | ✅ 是 (浏览器行为)         | 仅当域名匹配时                                                       |
| Session 数据       | ✅ 是 (依赖 sessionid)     | 需 sessionid Cookie 有效                                             |
| POST 数据          | ❌ 否                      | HTTP 301 会转为 GET 请求                                             |
| 请求头             | ❌ 否                      | 浏览器不会自动复制                                                   |
| URL 查询参数       | ❌ 否                      | 需手动添加到重定向 URL                                               |
| 认证信息           | ❌ 否                      | 除非使用 Cookie 存储或手动传递                                       |

### 4. 安全最佳实践
1. **敏感数据**：
   - 避免 URL 参数传递敏感信息（会被记录在浏览器历史、服务器日志中）
   - 使用 Session 或加密 Cookie

2. **跨域重定向**：
   ```python
   # 设置跨域 Cookie
   response = HttpResponsePermanentRedirect("https://other-domain.com/")
   response.set_cookie('key', 'value', 
                       domain='.example.com',  # 父域
                       samesite='None', 
                       secure=True)
   ```

3. **状态保持**：
   ```python
   # 使用 Django Session
   def login(request):
       request.session['user'] = username  # 存储
       return HttpResponsePermanentRedirect("/dashboard/")
   
   def dashboard(request):
       user = request.session.get('user')   # 重定向后可读取
   ```

### 5. 测试示例
```python
# views.py
def set_and_redirect(request):
    # 设置测试 Cookie
    response = HttpResponsePermanentRedirect("/show-data/")
    response.set_cookie('test_cookie', 'redirect_value')
    
    # 设置 Session
    request.session['test_session'] = 'session_data'
    return response

def show_data(request):
    # 读取数据
    cookie_data = request.COOKIES.get('test_cookie', 'Not found')
    session_data = request.session.get('test_session', 'Not found')
    
    return HttpResponse(f"""
        Cookie: {cookie_data}<br>
        Session: {session_data}
    """)
```

访问流程：
1. 访问 `/set-and-redirect/`
2. 被 301 重定向到 `/show-data/`
3. 显示：
   ```
   Cookie: redirect_value
   Session: session_data
   ```

### 结论
- **Cookies 和 Session** 会自动传递（依赖域名匹配）
- **其他请求数据不会自动传递**，需要手动处理
- 对于登录等场景，建议使用 Session 存储状态
- 避免在 URL 中传递敏感数据

如果需要完全保留请求状态，考虑：
```python
# 临时保存整个请求（不推荐）
request.session['original_request'] = {
    'method': request.method,
    'POST': request.POST.dict(),
    'GET': request.GET.dict()
}
return HttpResponsePermanentRedirect("/new-url/")
```
