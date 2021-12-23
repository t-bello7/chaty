from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from message.serializers import RoomSerializer, MessageSerializer
from message.models import Room, RoomMessage
from channels.layers import get_channel_layer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


User = get_user_model()
channel_layer = get_channel_layer

class RoomAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={201:'hey'},
        methods=["GET"]
    )
    def get(self, request):
        serializer_class = RoomSerializer
        queryrooms = Room.objects.all()
        return Response({'list':'retun list of rooms'})

    def post(self, request):
        serializer_class = RoomSerializer
        return Response({'post':'create new room'})

class MessagerAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get reccent messages
        """
        serializer_class = MessageSerializer
        return Response({'list' :'of messages'})
    def get(self, request, pk):
        """
            Get message by id
        """
        return Response({'one':'return one message'})
    def post(self, request):
        serializer_class = MessageSerializer
        return Response({'post': 'message'})
    def delete(self, response):
        serializer_class = MessageSerializer
        return Response({'delete':'message'})

# class ReceiptsAPIView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         serializer_class = RecieptSerialzer
#         return Response({'list':'readrecipts'})
#     def post(self, request):
#         serializer_class = RecieptSerialzer
#         return Response({'Update':'read receipt on message'})

