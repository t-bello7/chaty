from django.urls import path
from message.views import RoomAPIView, MessagerAPIView, ReceiptsAPIView

urlpatterns = [
    path('room/',RoomAPIView.as_view(), name='room'),
    path('room/<pk>/',RoomAPIView.as_view(), name=''),
    path('message/', MessagerAPIView.as_view(), name='message'),
    path('read_receipts', ReceiptsAPIView.as_view(), name='read_receipts')
]