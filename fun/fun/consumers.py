import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "global_room"
        self.room_group_name = "chat_%s" % self.room_name

        # Join the global group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
   # consumers.py

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # GET THE SENDER ID FROM THE JSON
        sender_id = text_data_json.get('sender_id')

        # Send message and sender_id to the global group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id # BROADCAST THE ID
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event.get('sender_id') # GET THE ID FROM THE EVENT

        # Send both back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))