import requests
from loguru import logger

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

# todo: 为了安全起见，需要在此处做权限认证，因为我发现，哪怕是基于 drf 框架的插件，权限居然用的不是 drf 的
# 不对，我只要保证我的所有接口都是 drf 实现的不就行了？如果用到了第三方插件，则需要验一下。
