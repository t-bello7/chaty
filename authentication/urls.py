from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

from authentication.views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,

)

urlpatterns = [
    path('register/', RegisterAPIView, name="register"),
    path('login/', LoginAPIView, name="'login"),
    path('logout/', LogoutAPIView, name="logout"),
]