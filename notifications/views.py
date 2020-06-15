import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import NotificationFilter
from .models import Notification
from .serializers import NotificationSerializer, NotificationDetailSerializer
# Create your views here.

class NotificationViewset(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    filter_class = NotificationFilter

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, unread=True)

    def get_serializer_class(self):
        if self.action == "update":
            return NotificationSerializer
        return NotificationDetailSerializer


class MarkAllNotificationView(APIView):
    def put(self, request):
        try:
            data = json.loads(request.body)
        except AttributeError:
            data = {}
        markall_read = bool(data.get("mark_all_as_read", None))
        markall_unread = bool(data.get("mark_all_as_unread", None))
        if all([markall_read, markall_unread]) or not any([markall_read, markall_unread]):
            return Response('Either `true` or `false` for one parameter in [ markall_read, markall_unread ]')

        is_allunread = markall_unread and not markall_read

        for notification in Notification.objects.filter(recipient=request.user):
            notification.unread = is_allunread
            notification.save()

        return Response('success')


def notification_handler(actor, recipient, verb, action_object, **kwargs):
    if actor.username != recipient.username and recipient.username == action_object.user.username:
        key = kwargs.get('key', 'notification')
        id_value = kwargs.get('id_value', None)

        instance = Notification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object=action_object
        )

        channel_layer = get_channel_layer()
        pay_load = {
            'type': 'receive',
            'key': key,
            'actor_name': actor.username,
            'action_object': action_object.user.username,
            'notification': NotificationDetailSerializer(instance).data,
            'id_value': id_value,
        }

        async_to_sync(channel_layer.group_send)('notifications', pay_load)
