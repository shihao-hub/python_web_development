from django.db import models
from django.conf import settings


class Course(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='讲师', on_delete=models.CASCADE,
                                help_text='课程讲师')

    name = models.CharField(verbose_name='名称', max_length=255, unique=True, help_text='课程名称')
    # TextField 似乎有默认值，空字符串
    introduction = models.TextField(verbose_name='介绍', help_text='课程介绍')
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text='课程价格')
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name
        ordering = ('price',)

    def __str__(self):
        return self.name
