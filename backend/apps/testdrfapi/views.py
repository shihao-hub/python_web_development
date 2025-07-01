from loguru import logger

from django.shortcuts import render
from django.http.request import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework import views, viewsets, decorators, permissions, status, generics, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# todo: 改为全局形式，应该又是 middleware
from apps.core import handle_unexpected_exception, SuccessResponse, ErrorResponse
from .serializers import GroupSerializer, UserSerializer, CourseSerializer
from .models import Course


# fixme: 不要使用 django api
def jupyternotebooks_test(request: WSGIRequest):
    # todo: 解决 iframe 提示 localhost 已拒绝连接这个问题
    return render(request, "jupyternotebooks_test.html", context={})


class UserModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer


# [example] ViewSet
class TestViewSet(viewsets.ViewSet):
    @decorators.action(detail=False, methods=['get'])
    @handle_unexpected_exception
    def test(self, request: Request) -> Response:
        return Response(status=200, data={"data": "test info"})


class CourseViewSet(viewsets.ViewSet):
    # 此处不兼容 <int:pk> 格式
    @decorators.action(detail=False, methods=["post"], url_path=r"get_and_delete/(?P<pk>\d+)")
    def get_and_delete(self, request: Request, pk: int):
        """ 获得并删除 """
        logger.info("get_and_delete")
        logger.info("pk: {}", pk)
        logger.info("request: {}", request)
        # todo: 抽取基本方法，如 get_object，因为 objects.get 找不到会出错
        inst = Course.objects.filter(pk=pk).first()
        if inst is None:
            return ErrorResponse("no such course")
        str_inst = CourseSerializer(instance=inst).data
        # inst.delete()
        return SuccessResponse(data={"data": str_inst})


# [example] DRF 的装饰器 api_view - 函数式编程
@decorators.api_view(["GET", "POST"])
@handle_unexpected_exception
def course_list(request: Request):
    """
    获取所有课程信息或者新增一个课程
    """
    # [note] drf Request 使用了组合，传入了 HttpRequest
    if request.method == "GET":
        # 序列化多个对象，所以需要 many=True
        s = CourseSerializer(instance=Course.objects.all(), many=True)
        # 序列化后的数据可以通过 s.data 获得
        return Response(data=s.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        # 反序列化，partial=True 表示部分更新
        s = CourseSerializer(data=request.data, partial=True)
        if s.is_valid():
            # 讲师是只读属性
            s.save(teacher=request.user)
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(["GET", "PUT", "DELETE"])
@handle_unexpected_exception
def course_detail(request: Request, pk: int):
    """
    获取、更新、删除一个课程
    """
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == "GET":
            # 序列化一个对象不需要 many=True
            s = CourseSerializer(instance=course)
            return Response(data=s.data, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            # PUT 方法表示更新，部分写法和 POST 方法类似
            # instance 是指要序列化哪个实例，data 表示数据哪里来的
            s = CourseSerializer(instance=course, data=request.data)
            # 表示把 data 的数据，反序列化之后，保存或者更新到 cuorse 对象里
            if s.is_valid():
                # 不需要 teacher 字段
                s.save()
                return Response(s.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# [example] DRF 中的视图 APIView - 类视图编程
class CourseList(views.APIView):
    """ 获取所有课程信息或新增一个课程 """

    def get(self, request):
        queryset = Course.objects.all()
        s = CourseSerializer(instance=queryset, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request):
        s = CourseSerializer(data=request.data)
        if s.is_valid():
            s.save(teacher=self.request.user)
            print(type(request.data), type(s.data))
            # type(request.data)： <class 'dict'>
            # type(s.data)： <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(views.APIView):
    """ 对单个课程进行 get、put、delete 操作 """

    @staticmethod
    def get_object(pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return

    def get(self, request, pk):
        obj = self.get_object(pk=pk)
        if not obj:
            return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
        s = CourseSerializer(instance=obj)
        return Response(s.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk=pk)
        if not obj:
            return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
        s = CourseSerializer(instance=obj, data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk=pk)
        if not obj:
            return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# [example] DRF 中的视图 GenericAPIView - 通用视图编程
class GCourseDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# 信号机制自动生成 Token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance=None, created=False, **kwargs):
    # 创建用户时自动生成 Token，注意 createsuperuser 命令似乎不会触发 post_save 信号，admin/ 页面上才会触发
    if created:
        logger.info("用户创建成功，自动生成 Token")
        Token.objects.create(user=instance)
