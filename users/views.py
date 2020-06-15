from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions

from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
# Create your views here.
class UserViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "update":
            return UserUpdateSerializer
        return UserSerializer

    # def get_permissions(self):
    #     if self.action == "retrieve":
    #         return [permissions.IsAuthenticated()]
    #     elif self.action == "create":
    #         return []
    #     return []

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None