from asgiref.sync import async_to_sync
from django.shortcuts import render, get_object_or_404
from channels.layers import get_channel_layer
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response

from users.models import User
from .models import Message
from .serializers import MessageSerializer, MessageDetailSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class MessageViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Message.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)

    def retrieve(self, request, pk=None):
        sender = self.request.user
        recipient = User.objects.filter(username=pk)
        if not recipient:
            return Response([], status=HTTP_404_NOT_FOUND)
        queryset = Message.objects.get_conversation(sender, recipient[0])
        serializer = MessageDetailSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # def get_queryset(self):
    #     """Combine queries from new, editor choice and popular"""
    #     new_qs = self.queryset.filter(new_place=True)[:self.slice_size]
    #     editor_qs = self.queryset.filter(editor_choice=True)[:self.slice_size]
    #     popular_qs = self.queryset.filter(popular=True)[:self.slice_size]

    #     return new_qs.union(editor_qs, popular_qs, all=True)

    def perform_create(self, serializer):
        messageObj = serializer.save()

        channel_layer = get_channel_layer()
        print(channel_layer)
        payload = {
            'type': 'receive',
            'message': messageObj.message,
            'sender': messageObj.sender.username
        }
        # group_send(group: 所在组-接收者的username, message: 消息内容)
        async_to_sync(channel_layer.group_send)("aaa", payload)
    
    def get_serializer_class(self):
        if self.action == "create":
            return MessageSerializer

        return MessageDetailSerializer
