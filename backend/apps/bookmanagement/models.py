from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    name = models.CharField(verbose_name="书籍名", max_length=100, db_index=True)
    # 【知识点】设置外键，设置 on_delete（CASCADE | PROTECT | SET_NULL | SET_DEFAULT | SET() | DO_NOTHING），设置 related_name（反向查询别名） # noqa
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="books", db_index=True)
    publisher = models.CharField(verbose_name="出版社", max_length=100)  # todo: 改为下拉框 + 可输入
    year = models.IntegerField(verbose_name="出版年")  # todo: 改为时间框弹出选择时间
    isbn = models.CharField(verbose_name="ISBN，国际标准书号", max_length=100, default="000-0-00-000000-0",
                            db_index=True)

    class Meta:
        verbose_name = verbose_name_plural = _("图书")

    def __str__(self):
        return self.name
