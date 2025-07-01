drf 的 BasicAuthentication 相关
```txt
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
```txt
    # todo: [to be confirmed] 确认一下为什么生产环境无法使用
    # DRF 的可浏览 API 认证
    # 用于测试和开发环境，生产环境应使用更安全的认证方式（Token, JWT 等）
    # api-auth/ 可以自由修改。登录视图：api-auth/login/，注销视图：api-auth/logout/
    # CSRF 风险：开发时启用的 session 认证可能带来 CSRF 漏洞（API 应使用无状态认证）
    path('debug/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
```

---
drf 的 authtoken
```txt
# urls.py
from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    # DRF 自带的 token 认证
    # 获取令牌的端点
    path('api-token-auth/', views.obtain_auth_token),
    
    # 其他路由...
]

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 可添加其他认证方式，如 Session 认证
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    # 可选的权限设置
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

rest_framework.authtoken 是 Django REST Framework (DRF) 提供的一个用于生成和验证用户认证令牌（Token）的模块。
它主要用于实现基于令牌的用户认证系统，允许客户端通过令牌而不是每次请求都发送用户名/密码进行身份验证。

默认情况下，令牌是永久有效的。如果需要实现令牌过期或刷新机制，需要自定义。

对于需要简单、快速实现 API 认证的系统，Token 认证是一个优秀的选择。
对于更复杂的需求（如令牌刷新、细粒度权限控制）， 可以考虑结合 JWT 或 OAuth2 实现更强大的认证授权系统。


---

SimpleUi 自定义菜单
```txt
# 自定义菜单
# 左侧可折叠菜单是 Simple UI 系统默认菜单
# 在大多数情况下，Simple UI 系统默认菜单不能满足需求，这时你就需要自定义菜单了，比如添加新的选项或给菜单选项分配新的图标

SIMPLEUI_CONFIG = {
    # 是否使用系统默认菜单。
    'system_keep': False,

    # 用于菜单排序和过滤, 不填此字段为默认排序和全部显示。 空列表 [] 为全部不显示.
    'menu_display': ['任务管理', '权限认证'],

    # 设置是否开启动态菜单, 默认为 False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': False,
    'menus': [
        {
            'app': 'auth',
            'name': '权限认证',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '用户列表',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': '用户组',
                    'icon': 'fa fa-th-list',
                    'url': 'auth/group/'
                }
            ]
        },
        {
            'name': '任务管理',
            'icon': 'fa fa-th-list',
            'models': [
                {
                    'name': '任务列表',
                    # 注意 url 按 /admin/ 应用名小写/模型名小写/ 命名。
                    'url': '/admin/tasks/task/',
                    'icon': 'fa fa-tasks'
                },
            ]
        },
    ]
}
```

---

