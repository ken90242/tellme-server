import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Notification
from .serializers import NotificationDetailSerializer

class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # if self.scope['user'].is_anonymous:
        #     await self.close()

        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """将接收到的消息返回给前端"""
        recipient = self.scope['user'].username
        # news动态发布时通知所有在线用户
        if text_data.get("key") == "additional_news":
            await self.send(text_data=json.dumps(text_data))
        sync_to_async(print(recipient))
        sync_to_async(print(text_data.get("actor_name")))
        sync_to_async(print(text_data.get("action_object")))
        # 只通知接收者，即recipient == 动作对象的作者
        if recipient != text_data.get("actor_name") and recipient == text_data.get("action_object"):
            await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        await self.channel_layer.group_discard("notifications", self.channel_name)
