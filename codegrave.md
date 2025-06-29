drf 的 BasicAuthentication 相关：
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Auth Type: Basic Auth
        # BasicAuthentication 默认不加密密码传输
        # 必须配合 HTTPS 使用（生产环境强制要求）
        # 不适合暴露在公共互联网的应用
        # 不适合存储敏感数据的应用
        # fixme: 不要使用这个，而且不知道为什么加了这个之后，drf 的登出失效了。。。
        # 'rest_framework.authentication.BasicAuthentication',
    ]
}

```

---

drf 的 api-auth
```python
    # todo: [to be confirmed] 确认一下为什么生产环境无法使用
    # DRF 的可浏览 API 认证
    # 用于测试和开发环境，生产环境应使用更安全的认证方式（Token, JWT 等）
    # api-auth/ 可以自由修改。登录视图：api-auth/login/，注销视图：api-auth/logout/
    # CSRF 风险：开发时启用的 session 认证可能带来 CSRF 漏洞（API 应使用无状态认证）
    path('debug/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
```