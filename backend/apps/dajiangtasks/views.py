from typing import Annotated

from django.urls import reverse
from loguru import logger

from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http.request import HttpRequest

from . import models, forms


class NotAllowedMethodJsonResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        super().__init__({"message": "请求方法不允许"},
                         *args,
                         status=400,
                         json_dumps_params={"ensure_ascii": False},
                         **kwargs)


class SuccessJsonResponse(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data,
                         *args,  # todo: 确定一下 data 与 *args 的顺序发生变化怎么办？考虑第三方库的不同版本啊
                         status=200,
                         safe=False,
                         json_dumps_params={"ensure_ascii": False},
                         **kwargs)


class ErrorJsonResponse(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data,
                         *args,
                         status=400,
                         safe=False,
                         json_dumps_params={"ensure_ascii": False},
                         **kwargs)


def is_json_content_type(request: HttpRequest):
    return request.content_type == "application/json"


class TaskViews:
    # todo: 为什么 get 不需要权限认证？（drf 全局设置后，get 也需要认证）
    def task_list(self, request: Annotated[HttpRequest, "django Base Request"]):
        """列出任务列表"""
        if request.method not in ["GET"]:
            return NotAllowedMethodJsonResponse()  # 暂且如此使用，原始 django 还是前后端不分离开发的好

        tasks = models.Task.objects.all()
        return render(request, "dajiangtasks/dajiangtasks_list.html", {"tasks": tasks, })

    # todo: 为什么 post 需要权限认证？我使用的原始 django 呀。NO，是请求的表头需要携带 X-CSRFToken | @csrf_exempt 禁用 CSRF
    def task_create(self, request: HttpRequest):
        """创建任务"""
        if request.method not in ["GET", "POST"]:
            return NotAllowedMethodJsonResponse()

        if request.method == "POST":
            form = forms.TaskForm(request.POST)
            if form.is_valid():
                form.save()
                # 表单有效，跳转到任务列表页
                return redirect(reverse("dajiangtasks:task_list"))
        # 如果表单无效，或者 GET 请求，则跳转到空表单页面
        form = forms.TaskForm()
        return render(request, "dajiangtasks/dajiangtasks_form.html", {"form": form, })

    def task_delete(self, request: HttpRequest, pk: int):
        """删除某条任务"""
        # 注意，没有 DELETE，目前的理解，原始 django 似乎只使用 GET 和 POST？
        # 目前在我看来，需要传多一点的数据那就是 POST，大部分场景一个是表单（少部分一个是 ajax 调用）？
        # todo: 需要确定一下理解的如何
        if request.method not in ["GET"]:  # "DELETE" 不能用...
            return NotAllowedMethodJsonResponse()

        obj = get_object_or_404(models.Task, pk=pk)
        obj.delete()
        return redirect(reverse("dajiangtasks:task_list"))

    def task_update(self, request: HttpRequest, pk: int):
        """更新某条任务的详情"""
        if request.method not in ["GET", "POST"]:  # todo: "PUT" 呢？
            return NotAllowedMethodJsonResponse()

        obj = get_object_or_404(models.Task, pk=pk)
        form = forms.TaskForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # 表单有效，跳转到任务详情页
            return redirect(reverse("dajiangtasks:task_detail", args=[pk, ]))

        # 填写的无效，回到表单页面，但是携带了数据
        form = forms.TaskForm(instance=obj)
        return render(request, "dajiangtasks/dajiangtasks_form.html", {"form": form, "object": obj})

    def task_detail(self, request: HttpRequest, pk: int):
        """列出某条任务的详情"""
        if request.method not in ["GET"]:
            return NotAllowedMethodJsonResponse()
        task = get_object_or_404(models.Task, pk=pk)
        return render(request, "dajiangtasks/dajiangtasks_detail.html", {"task": task, })
