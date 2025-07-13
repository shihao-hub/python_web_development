from django.db import models


class User(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=10)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
