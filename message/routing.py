from django.conf.urls import url
from message.consumers import ChatConsumer

websocket_urlpatterns = [
    url(r'^ws/message/(?P<room_name>\w+)/$', ChatConsumer.as_asgi())
]