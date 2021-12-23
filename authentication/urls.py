from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from authentication.views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,

)

urlpatterns = [
    path('token/', obtain_auth_token, name='obtain-token'),
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
]