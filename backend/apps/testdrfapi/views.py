from django.http.request import HttpRequest
from django.contrib.auth.models import Group, User
from rest_framework import views, viewsets, decorators, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core import handle_unexpected_exception
from .serializers import GroupSerializer, UserSerializer, CourseSerializer
from .models import Course


class UserModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestViewSet(viewsets.ViewSet):
    @handle_unexpected_exception
    @decorators.action(url_path="test", detail=False, methods=['get'])
    def test(self, request: Request) -> Response:
        return Response(status=200, data={"data": "test info"})


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


class CourseList(views.APIView):
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
