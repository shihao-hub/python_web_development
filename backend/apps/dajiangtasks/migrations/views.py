from loguru import logger

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http.request import HttpRequest

from . import models, forms


# todo: 为什么 get 不需要权限认证？
def task_list(request: HttpRequest):
    """列出任务列表"""
    if request.method not in ["GET"]:
        return JsonResponse({"message": "请求方法不允许"}, status=400, json_dumps_params={"ensure_ascii": False})
    tasks = models.Task.objects.all()
    # todo: 需要过滤
    data = serializers.serialize("json", tasks)
    return JsonResponse(data, status=200, safe=False, json_dumps_params={"ensure_ascii": False})


# todo: 为什么 post 需要权限认证？我使用的原始 django 呀。
def task_create(request: HttpRequest):
    """创建任务"""
    if request.method not in ["POST"]:
        return JsonResponse({"message": "请求方法不允许"}, status=400, json_dumps_params={"ensure_ascii": False})
    form = forms.TaskForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"message": form.errors}, status=400, json_dumps_params={"ensure_ascii": False})
    form.save()
    return JsonResponse({"message": "创建成功"}, status=200, json_dumps_params={"ensure_ascii": False})


def task_update(request: HttpRequest):
    """更新某条任务的详情"""


def task_delete(request: HttpRequest):
    """删除某条任务"""


def task_detail(request: HttpRequest):
    """列出某条任务的详情"""
