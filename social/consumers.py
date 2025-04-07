import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_username = data['username']
        receiver_username = data['receiver']
        message = data['message']

        sender = await sync_to_async(User.objects.get)(username=sender_username)
        receiver = await sync_to_async(User.objects.get)(username=receiver_username)

        # Save message to the database
        await sync_to_async(ChatMessage.objects.create)(
            sender=sender,
            receiver=receiver,
            message=message
        )

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "username": sender_username,
                "receiver": receiver_username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "receiver": event["receiver"]
        }))
