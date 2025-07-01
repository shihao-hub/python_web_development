# 覆盖 Django REST Framework 的登录模板指南

要覆盖 DRF 的默认登录页面，你可以通过创建自定义模板文件来实现。以下是完整的实现步骤：

## 步骤 1: 创建模板目录结构

在你的 Django 项目中创建以下目录结构：

```
your_project/
├── templates/
│   └── rest_framework/
│       ├── login.html       # 主登录模板
│       └── base.html        # 可选：覆盖基础模板
```

## 步骤 2: 创建自定义登录模板

创建 `templates/rest_framework/login.html` 文件：

```html
{% extends "rest_framework/base.html" %}

{% block title %}柔性配电评估系统 - 登录{% endblock %}

{% block branding %}
    <h3 style="margin: 0 0 20px; color: #1a5276;">
        <i class="fa fa-bolt" aria-hidden="true"></i>
        柔性配电评估系统
    </h3>
{% endblock %}

{% block content %}
<div class="container-fluid" style="margin-top: 30px">
    <div class="row">
        <div class="col-md-6 col-md-offset-3">
            <div class="panel panel-default" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div class="panel-heading" style="background: linear-gradient(135deg, #1a5276, #2874a6); color: white; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                    <h3 class="panel-title" style="font-size: 18px; font-weight: 600;">系统登录</h3>
                </div>
                
                <div class="panel-body" style="padding: 30px;">
                    <form action="{% url 'rest_framework:login' %}" role="form" method="post">
                        {% csrf_token %}
                        <input type="hidden" name="next" value="{{ next }}" />
                        
                        <div class="form-group">
                            <label for="username" style="font-weight: 500; color: #2c3e50;">用户名</label>
                            <input type="text" class="form-control input-lg" id="username" name="username" 
                                placeholder="请输入用户名" style="border-radius: 4px; border: 1px solid #ddd; padding: 12px;">
                        </div>
                        
                        <div class="form-group">
                            <label for="password" style="font-weight: 500; color: #2c3e50;">密码</label>
                            <input type="password" class="form-control input-lg" id="password" name="password" 
                                placeholder="请输入密码" style="border-radius: 4px; border: 1px solid #ddd; padding: 12px;">
                        </div>
                        
                        {% if form.errors %}
                        <div class="alert alert-danger" style="border-radius: 4px; padding: 10px 15px;">
                            <i class="fa fa-exclamation-circle" aria-hidden="true"></i>
                            用户名或密码不正确
                        </div>
                        {% endif %}
                        
                        <div class="form-group" style="margin-top: 25px;">
                            <button type="submit" class="btn btn-primary btn-block btn-lg" 
                                style="background: linear-gradient(135deg, #1a5276, #2874a6); border: none; border-radius: 4px; padding: 12px; font-weight: 600;">
                                <i class="fa fa-sign-in" aria-hidden="true"></i> 登 录
                            </button>
                        </div>
                    </form>
                    
                    <div class="text-center" style="margin-top: 20px; color: #7f8c8d;">
                        <p>© 2023 柔性配电评估系统 | 版本 1.0.0</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block style %}
    {{ block.super }}
    <style>
        body {
            background: #f5f7fa;
            background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
        }
        
        .navbar {
            display: none;
        }
        
        .panel {
            border: none;
            margin-top: 50px;
        }
        
        .btn-primary:hover {
            background: linear-gradient(135deg, #154360, #1a5276);
            box-shadow: 0 4px 8px rgba(26, 82, 118, 0.3);
        }
        
        .form-control:focus {
            border-color: #3498db;
            box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
        }
        
        @media (max-width: 768px) {
            .col-md-6 {
                width: 90%;
                margin-left: 5%;
            }
        }
    </style>
{% endblock %}
```

## 步骤 3: 覆盖基础模板（可选）

如果你想进一步自定义整个 DRF 界面的样式，可以覆盖基础模板：

创建 `templates/rest_framework/base.html`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    {% block head %}
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <title>{% block title %}{% if name %}{{ name }} – {% endif %}柔性配电评估系统 API{% endblock %}</title>
    
    {% block style %}
    <link rel="stylesheet" type="text/css" href="{% static "rest_framework/css/bootstrap.min.css" %}"/>
    <link rel="stylesheet" type="text/css" href="{% static "rest_framework/css/bootstrap-tweaks.css" %}"/>
    <link rel="stylesheet" type="text/css" href="{% static "rest_framework/css/prettify.css" %}"/>
    <link rel="stylesheet" type="text/css" href="{% static "rest_framework/css/default.css" %}"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        /* 自定义全局样式 */
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }
        
        .navbar {
            background: linear-gradient(135deg, #1a5276, #2874a6);
            border: none;
            border-radius: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            color: white !important;
            font-weight: 600;
            font-size: 18px;
        }
        
        .navbar-text {
            color: rgba(255,255,255,0.8) !important;
        }
        
        .breadcrumb {
            background-color: transparent;
            padding: 8px 15px;
            margin-bottom: 20px;
            border-radius: 4px;
            background-color: #e9f7fe;
            border-left: 4px solid #3498db;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #1a5276, #2874a6);
            border: none;
            border-radius: 4px;
        }
        
        .btn-primary:hover {
            background: linear-gradient(135deg, #154360, #1a5276);
            box-shadow: 0 4px 8px rgba(26, 82, 118, 0.3);
        }
        
        .panel-heading {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-bottom: 1px solid #dee2e6;
            font-weight: 600;
        }
    </style>
    {% endblock %}
    
    {% endblock %}
</head>

<body class="{% block bodyclass %}{% endblock %}">

{% block body %}
<div class="wrapper">
    {% block navbar %}
    <div class="navbar navbar-static-top {% block bootstrap_navbar_variant %}navbar-inverse{% endblock %}">
        <div class="container">
            <span>
                {% block branding %}
                <a class="navbar-brand" rel="nofollow" href="/">
                    <i class="fa fa-bolt" aria-hidden="true"></i>
                    柔性配电评估系统 API
                </a>
                {% endblock %}
            </span>
            
            <ul class="nav navbar-nav pull-right">
                {% block userlinks %}
                {% if user.is_authenticated %}
                {% optional_logout request user %}
                {% else %}
                {% optional_login request %}
                {% endif %}
                {% endblock %}
            </ul>
        </div>
    </div>
    {% endblock %}
    
    <div class="container">
        {% block breadcrumbs %}
        <ul class="breadcrumb">
            {% for breadcrumb_name, breadcrumb_url in breadcrumblist %}
            {% if forloop.last %}
            <li class="active"><a href="{{ breadcrumb_url }}">{{ breadcrumb_name }}</a></li>
            {% else %}
            <li><a href="{{ breadcrumb_url }}">{{ breadcrumb_name }}</a> <span class="divider">&rsaquo;</span></li>
            {% endif %}
            {% empty %}
            {% block breadcrumbs_empty %}&nbsp;{% endblock breadcrumbs_empty %}
            {% endfor %}
        </ul>
        {% endblock %}
        
        <!-- 内容块 -->
        {% block content %}{% endblock %}
    </div>
</div>

<!-- 脚本 -->
{% block script %}
<script src="{% static "rest_framework/js/jquery-3.5.1.min.js" %}"></script>
<script src="{% static "rest_framework/js/ajax-form.js" %}"></script>
<script src="{% static "rest_framework/js/csrf.js" %}"></script>
<script src="{% static "rest_framework/js/bootstrap.min.js" %}"></script>
<script src="{% static "rest_framework/js/prettify-min.js" %}"></script>
<script src="{% static "rest_framework/js/default.js" %}"></script>
<script>
    // 自定义脚本
    $(document).ready(function() {
        // 添加登录表单自动聚焦
        $('#username').focus();
        
        // 添加回车键提交功能
        $('input').keypress(function(e) {
            if (e.which == 13) {
                $('form').submit();
                return false;
            }
        });
    });
</script>
{% endblock %}

{% endblock %}
</body>
</html>
```

## 步骤 4: 配置模板路径和静态文件

在 `settings.py` 中确保模板配置正确：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # 添加模板目录
        ],
        'APP_DIRS': True,
        # ...
    },
]

# 静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

## 步骤 5: 添加自定义 CSS 和图标（可选）

在 `static/css/custom.css` 中添加额外的样式：

```css
/* 自定义登录页面样式 */
.login-container {
    max-width: 450px;
    margin: 50px auto;
    padding: 30px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.login-header {
    text-align: center;
    margin-bottom: 30px;
}

.login-header h2 {
    color: #1a5276;
    font-weight: 600;
    margin-bottom: 10px;
}

.login-header p {
    color: #7b8a8b;
    font-size: 16px;
}

.login-footer {
    text-align: center;
    margin-top: 20px;
    color: #7f8c8d;
    font-size: 14px;
}

.password-reset-link {
    display: block;
    text-align: right;
    margin-top: -10px;
    margin-bottom: 20px;
    color: #3498db;
    font-size: 14px;
}
```

## 步骤 6: 自定义登录视图（高级选项）

如果你想完全控制登录逻辑，可以创建自定义登录视图：

```python
# api/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy

class CustomLoginView(FormView):
    template_name = 'rest_framework/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('api-root')  # 替换为你的API根路径
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            
            # 记录登录日志
            LoginLog.objects.create(
                user=user,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
            
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['system_name'] = "柔性配电评估系统"
        context['system_version'] = "1.5.0"
        return context
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

# urls.py
from .views import CustomLoginView

urlpatterns = [
    # ...
    path('api-auth/login/', CustomLoginView.as_view(), name='custom-login'),
]
```

## 步骤 7: 在设置中配置自定义登录URL

```python
# settings.py

# 使用自定义登录URL
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'LOGIN_URL': 'custom-login',  # 指向自定义登录视图
    'LOGOUT_URL': 'rest_framework:logout',
}
```

## 高级自定义选项

### 1. 添加多因素认证

```python
# views.py
from django_otp import login as otp_login
from django_otp.plugins.otp_totp.models import TOTPDevice

class CustomLoginView(FormView):
    # ... 之前的代码 ...
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 检查是否启用了双因素认证
            if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
                # 存储用户ID用于后续验证
                self.request.session['otp_user_id'] = user.id
                # 重定向到OTP验证页面
                return redirect('otp-verify')
            
            login(self.request, user)
            # ... 记录日志 ...
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
```

### 2. 添加验证码支持

```python
# forms.py
from django import forms
from captcha.fields import CaptchaField

class CaptchaLoginForm(AuthenticationForm):
    captcha = CaptchaField(
        label='验证码',
        error_messages={'invalid': '验证码错误'}
    )

# views.py
class CustomLoginView(FormView):
    form_class = CaptchaLoginForm  # 使用带验证码的表单
    # ...
```

### 3. 添加社交登录选项

在模板中添加社交登录按钮：

```html
<div class="social-login">
    <p class="text-center" style="margin: 20px 0 10px; color: #7f8c8d;">
        <span>或使用其他方式登录</span>
    </p>
    
    <div class="row">
        <div class="col-xs-4">
            <a href="{% url 'social:begin' 'github' %}" class="btn btn-block btn-social btn-github">
                <i class="fab fa-github"></i> GitHub
            </a>
        </div>
        <div class="col-xs-4">
            <a href="{% url 'social:begin' 'google-oauth2' %}" class="btn btn-block btn-social btn-google">
                <i class="fab fa-google"></i> Google
            </a>
        </div>
        <div class="col-xs-4">
            <a href="{% url 'social:begin' 'weibo' %}" class="btn btn-block btn-social btn-weibo">
                <i class="fab fa-weibo"></i> 微博
            </a>
        </div>
    </div>
</div>

<style>
.btn-social {
    position: relative;
    padding: 10px;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    border-radius: 4px;
    color: white;
    margin-bottom: 10px;
}

.btn-github { background: #444; }
.btn-google { background: #dd4b39; }
.btn-weibo { background: #e6162d; }

.btn-social i {
    font-size: 18px;
    margin-right: 5px;
    vertical-align: middle;
}
</style>
```

## 最佳实践建议

1. **响应式设计**：
   - 使用 Bootstrap 的响应式类确保在各种设备上都能良好显示
   - 添加移动端特定的样式调整

2. **安全性增强**：
   ```html
   <!-- 在表单中添加CSRF令牌 -->
   {% csrf_token %}
   
   <!-- 添加登录尝试限制 -->
   <script>
   $(document).ready(function() {
       let attemptCount = 0;
       $('form').submit(function() {
           attemptCount++;
           if (attemptCount > 3) {
               // 显示验证码或锁定提示
               $('#captcha-container').show();
           }
       });
   });
   </script>
   ```

3. **可访问性优化**：
   - 为所有表单元素添加适当的标签
   - 确保颜色对比度符合 WCAG 标准
   - 添加键盘导航支持

4. **性能优化**：
   - 压缩 CSS 和 JavaScript
   - 使用 CDN 加载字体和图标
   - 添加浏览器缓存控制

5. **品牌一致性**：
   - 使用企业品牌颜色和标识
   - 保持与主应用相同的设计语言
   - 添加版权信息和版本号

通过以上步骤，你可以完全自定义 Django REST Framework 的登录页面，使其与你的应用风格一致，并添加所需的功能增强。
