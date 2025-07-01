from django.apps import AppConfig


class TempConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.testdrfapi'
    verbose_name = "测试 - drf api"
