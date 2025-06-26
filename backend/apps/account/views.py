from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status, routers, decorators, views, viewsets
from rest_framework.response import Response

from .serializers import UserLoginSerializer, UserSerializer


class LoginLogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @decorators.action(detail=False, methods=['post'], url_path="login/")
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=False, methods=['post'], url_path="login/")
    def logout(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


class UserDetailModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer


router = routers.DefaultRouter()
# todo: [to be understood] why the router is not working(api doc is not showing)
router.register(r"loginlogout", LoginLogoutViewSet, basename="login-logout")
router.register(r"userdetail", UserDetailModelViewSet)
