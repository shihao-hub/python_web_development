from django_filters import rest_framework as rest_framework_filters

from . import models


# 【知识点】django_filters，让过滤如此简单
class BookFilter(rest_framework_filters.FilterSet):
    """
    使用笔记：
        1. FilterSet 要使用 django_filters.rest_framework.FilterSet
        2. View 中要使用 filterset_class 而不是 filter_class
        3. 查询字段 a,b,c，查询参数 a=1&b=&c= 似乎就是 a=1？不确定，毕竟 "" 确实可以匹配任何字符串
    待办事项：
        1. 进一步了解如何使用 django-filters，目前已掌握基础使用，大多数场景也就是这么基础而已

    """
    name = rest_framework_filters.CharFilter(field_name="name", lookup_expr="icontains")
    publisher = rest_framework_filters.CharFilter(field_name="publisher", lookup_expr="icontains")

    class Meta:
        model = models.Book
        fields = ("name", "author", "publisher", "year")
