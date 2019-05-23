from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

GROUP_NAME = 'chat'


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            GROUP_NAME,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            GROUP_NAME,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            GROUP_NAME,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user'] if event['user'] else 'anonymous user'

        await self.send(text_data=json.dumps(
            {
                'message': message,
                'user': user
            })
        )
