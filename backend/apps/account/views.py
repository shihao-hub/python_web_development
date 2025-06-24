
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import UserLoginSerializer, UserSerializer


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# 传统视图用于渲染登录页面
def login_view(request):
    return render(request, 'rest_framework/login.html')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')
