# Django modules
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

#Rest Framework Modules
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from authentication.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
# Create your views here.

User = get_user_model()

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register API for registering users 
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
           serializer.save()
           user_data = serializer.data
           user = User.objects.get(email=user_data['email'])
           token = Token.objects.get(user).key
           user_data['token'] = token
           return Response(user_data, status=status.HTTP_201_created)
        return Response(serializer.default_error_messages['invalid'], status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Login API for authenticating users
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       


class LogoutAPIView(GenericAPIView):
    """Logout API for logging out users"""
     
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
