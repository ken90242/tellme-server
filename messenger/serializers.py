from rest_framework import serializers
from django.db.models import Q

from users.serializers import UserSerializer
from .models import Message


class MessageDetailSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Message
        fields = "__all__"
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender", "recipient", "message"]