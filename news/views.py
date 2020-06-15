from django.shortcuts import render

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions

from .models import News
from .serializers import NewsSerializer, NewsDetailSerializer, NewsLikeOPSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from notifications.views import notification_handler
# Create your views here.
class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.filter(parent=None)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ["create", "delete"]:
            return [permissions.IsAuthenticated()]
        return []
    
    def get_serializer_class(self):
        if self.action == "create":
            return NewsSerializer
        elif self.action == "update":
            return NewsLikeOPSerializer
        return NewsDetailSerializer
    
    def perform_create(self, serializer):
        new_instance = serializer.save()
        if new_instance.reply:
            parent = new_instance.parent if new_instance.parent else new_instance
            notification_handler(new_instance.user, parent.user, 'R', parent, id_value=str(parent.uuid_id), key='social_update')

    def perform_update(self, serializer):
        """do what switch like do"""
        new_instance = serializer.save()
        if new_instance.user.username != self.request.user.username and\
            self.request.user in new_instance.liked.all():
            notification_handler(self.request.user, new_instance.user, 'L', new_instance, id_value=str(new_instance.uuid_id), key='social_update')