from rest_framework import serializers
from message.models import Room , RoomMessage

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','title', 'first_user','second_user']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessage
        fields = ['id','user', 'room','content']

