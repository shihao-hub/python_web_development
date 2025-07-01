import overrides
from django.shortcuts import render
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import (
    # 数据显示视图
    RedirectView, TemplateView, ListView, DetailView,
    # 数据操作视图
    FormView, CreateView, UpdateView, DeleteView,
    # 日期筛选视图
    ArchiveIndexView, YearArchiveView, MonthArchiveView,
    WeekArchiveView, DayArchiveView, TodayArchiveView, DateDetailView
)


class TestTemplateView(TemplateView):
    """ TemplateView 只定义了 get 方法 """
    template_name = "index.html"
    template_engine = None  # 默认 settings.TEMPLATES.BACKEND
    content_type = None  # 默认 text/html
    extra_context = {"title": "首页", "class_content": ""}  # 顾名思义，存放比较固定的 context

    @overrides.override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({})
        return context
