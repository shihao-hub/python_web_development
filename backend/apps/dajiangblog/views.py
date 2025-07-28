from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import (
    ListView,  # 展示对象列表
    DetailView,  # 查看某个对象的详细信息
    CreateView,  # 通过表单创建某个对象
    UpdateView,  # 通过表单更新某个对象信息
    FormView,  # 用户填写表单提交后转到某个完成页面
    DeleteView,  # 删除某个对象
)

from . import models


class IndexView(ListView):
    model = models.Article


class ArticleDetailView(DetailView):
    model = models.Article


class ArticleDelete(DeleteView):
    model = models.Article
    success_url = reverse_lazy('index')