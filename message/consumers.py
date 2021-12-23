import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from message.models import Room, RoomMessage

User = get_user_model()
class ChatConsumer(AsyncJsonWebSocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room-name']
        self.room_group_name = 'room_%s' % self.room_name
         
        # Join room group 
        message_obj = await self.get_messages(room_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_message(self, text_data):
        """
        Recieve message from WebSocket.
        Get the event and send the appropraite event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)

     

    async def receieve(self, res):
        """
        Receive message from room group
        """
        await self.send(text_data=json.dumps({
            "payload": res,
        }))

    @database_sync_to_async
    def get_messages(self, room):
        messages = RoomMessage.objects.by_room(room)[1]
        return messages

    @database_sync_to_async
    def create_room_message(self, user, msg):
        return RoomMessage.objects.create(user=user, room=room, content=message)


