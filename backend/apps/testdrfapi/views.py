from django.contrib.auth.models import Group, User
from rest_framework import views, viewsets, decorators, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core import handle_unexpected_exception
from .serializers import GroupSerializer, UserSerializer


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
    # @handle_unexpected_exception
    @decorators.action(url_path="test", detail=False, methods=['get'])
    def test(self, request: Request) -> Response:
        return Response(status=200, data={"data": "test info"})
