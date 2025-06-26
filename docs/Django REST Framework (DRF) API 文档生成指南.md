# Django REST Framework (DRF) API 文档生成指南

在 Django REST Framework (DRF) 中，自动生成 API 文档是提高开发效率和 API 可维护性的重要功能。以下是几种主要的 API 文档生成方法：

## 1. 内置的 API 文档生成

### 基本配置

在 `settings.py` 中添加：

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.documentation',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
```

在 `urls.py` 中添加文档路由：

```python
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # ...
    path('docs/', include_docs_urls(title='API Documentation')),
]
```

### 在视图中添加文档

```python
class UserList(APIView):
    """
    get:
    返回所有用户列表
    
    post:
    创建新用户
    
    ### 示例请求
    ```json
    {
        "username": "newuser",
        "email": "user@example.com"
    }
    ```
    """
    
    def get(self, request):
        """返回用户列表的具体实现"""
        # ...
    
    def post(self, request):
        # ...
```

## 2. 使用第三方库 drf-yasg (Swagger/OpenAPI)

### 安装
```bash
pip install drf-yasg
```

### 配置

在 `settings.py` 中：
```python
INSTALLED_APPS = [
    # ...
    'drf_yasg',
]
```

在 `urls.py` 中：
```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API 文档描述",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ...
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### 自定义文档内容

```python
from drf_yasg.utils import swagger_auto_schema

class UserDetail(APIView):
    @swagger_auto_schema(
        operation_description="获取用户详细信息",
        responses={
            200: UserSerializer(),
            404: "用户未找到"
        },
        manual_parameters=[
            openapi.Parameter(
                'fields',
                openapi.IN_QUERY,
                description="指定返回字段",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, user_id):
        # ...
```

## 3. 使用 drf-spectacular (OpenAPI 3.0)

### 安装
```bash
pip install drf-spectacular
```

### 配置

在 `settings.py` 中：
```python
INSTALLED_APPS = [
    # ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Documentation',
    'DESCRIPTION': 'API 文档描述',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

在 `urls.py` 中：
```python
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # ...
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

### 自定义文档内容

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    description='获取用户详细信息',
    parameters=[
        OpenApiParameter(
            name='fields',
            type=str,
            location=OpenApiParameter.QUERY,
            description='指定返回字段',
        ),
    ],
    responses=UserSerializer,
)
def retrieve(self, request, *args, **kwargs):
    # ...
```

## 4. 最佳实践与技巧

### 1. 文档注释规范
- 使用 Markdown 格式编写详细描述
- 为每个 HTTP 方法添加说明
- 包含请求和响应示例
- 解释参数的作用和格式

### 2. 序列化器文档
```python
class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    
    ### 字段说明
    - id: 用户唯一标识
    - username: 用户名 (4-20字符)
    - email: 电子邮箱 (必须有效)
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {
            'username': {'help_text': '4-20个字符，只能包含字母、数字和下划线'},
            'email': {'help_text': '有效的电子邮箱地址'},
        }
```

### 3. 模型文档
```python
class User(models.Model):
    """
    系统用户
    
    ### 字段说明
    - username: 用户名
    - email: 电子邮箱
    - created_at: 账户创建时间
    """
    username = models.CharField(max_length=20, help_text='4-20个字符')
    email = models.EmailField(help_text='有效的电子邮箱地址')
    created_at = models.DateTimeField(auto_now_add=True)
```

### 4. 文档安全配置
```python
# drf-yasg 配置 JWT 认证
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# drf-spectacular 配置 JWT 认证
SPECTACULAR_SETTINGS = {
    'SECURITY': [{'Bearer': []}],
    'SERVERS': [{'url': 'https://api.example.com', 'description': '生产环境'}],
}
```

## 5. 文档部署与维护

### 自动化部署
- 将文档生成集成到 CI/CD 流程中
- 使用 GitHub Pages 或 Read the Docs 托管文档
- 每次发布新版本时自动更新文档

### 版本控制
```python
# 多版本 API 文档支持
urlpatterns = [
    path('v1/docs/', include_docs_urls(title='API v1 Documentation', public=False)),
    path('v2/docs/', include_docs_urls(title='API v2 Documentation', public=False)),
]
```

### 文档测试
- 使用 Postman 或 Insomnia 测试 API
- 使用 DRF 的 APITestCase 编写测试用例
- 确保文档与实际 API 行为一致

## 比较表

| 特性 | 内置文档 | drf-yasg | drf-spectacular |
|------|----------|----------|-----------------|
| OpenAPI 版本 | 2.0 | 2.0 | 3.0 |
| Swagger UI 支持 | ✓ | ✓ | ✓ |
| ReDoc 支持 | ✓ | ✓ | ✓ |
| 自定义程度 | 中 | 高 | 高 |
| 安装复杂度 | 低 | 中 | 中 |
| 自动字段检测 | 基础 | 良好 | 优秀 |
| 枚举支持 | 有限 | 良好 | 优秀 |
| 认证集成 | 基础 | 良好 | 优秀 |
| 最新维护 | 一般 | 良好 | 优秀 |

## 结论

对于大多数项目，推荐使用 **drf-spectacular**，因为它：
1. 支持最新的 OpenAPI 3.0 规范
2. 提供更准确的自动文档生成
3. 有更好的枚举和认证支持
4. 持续维护和更新

对于简单项目或不需要复杂文档的场景，DRF 内置文档可能是更轻量级的选择。

无论选择哪种方案，关键是要：
- 保持文档与实际代码同步
- 提供详细的示例和使用说明
- 定期更新文档并确保其准确性
- 将文档生成集成到开发流程中

良好的 API 文档可以显著提高开发效率，减少集成问题，并改善团队协作体验。
