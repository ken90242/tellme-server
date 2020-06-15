#!/usr/bin/python3
# -*- coding:utf-8 -*-
from datetime import datetime

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler

from .models import Message
from .serializers import MessageSerializer

class MessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        
        await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)
        await self.accept()
        await self.send(text_data="connected")

    async def receive_json(self, content, **kwargs):
        # sender = self.scope['user']
        sender = self.scope['user']
        recipient = await self.get_user_by_name(content['recipientName'])
        if sender != recipient:
            await self.create_message(sender, recipient, content['message'])

            payload = {
                'type': 'chat_broadcast',
                'message': {
                    'message': content["message"],
                    'created_at': str(datetime.now()),
                    'sender': {
                        'username': sender.username,
                    },
                }
            }

            # aaa -> recipient.name
            await self.channel_layer.group_send(recipient.username, payload)

    async def disconnect(self, code):
        # aaa -> self.scope['user']
        await self.channel_layer.group_discard("root", self.channel_name)
    
    async def chat_broadcast(self, event):
        await self.send_json(event)
    
    @database_sync_to_async
    def get_user_by_name(self, username):
        result = get_user_model().objects.filter(username=username)
        if result:
            return result[0]
        return None
    
    @database_sync_to_async
    def create_message(self, sender, recipient, message):
        sync_to_async(print(sender.username, recipient.username))
        msg = MessageSerializer(
            data={
                'sender': sender.id,
                'recipient': recipient.id,
                'message': message
            }
        )

        if msg.is_valid():
            msg.save()
