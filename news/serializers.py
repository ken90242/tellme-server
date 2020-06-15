from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from news.models import News
from users.serializers import UserSerializer, checkUserAuthSerializer
from django.contrib.auth import get_user_model

User = get_user_model()



class ChildNewsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = News
        fields = "__all__"

class NewsDetailSerializer(serializers.ModelSerializer):
    thread = ChildNewsSerializer(many=True)
    liked = checkUserAuthSerializer(many=True)
    user = UserSerializer()
    class Meta:
        model = News
        fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):
    parent_uuid = serializers.CharField(required=False, max_length=36, write_only=True)
    class Meta:
        model = News
        fields = ["content", "parent_uuid"]
        # fields = ["content", "parent", "reply"]
    
    def validate(self, attrs):
        if 'parent_uuid' in attrs:
            parent_news = News.objects.filter(uuid_id=attrs.pop('parent_uuid'))
            if not parent_news:
                raise ValidationError("Cannot find reply topic")
                
            attrs["parent"] = parent_news[0]

            if attrs["parent"] and attrs["parent"].parent != None:
                raise ValidationError("Cannot reply to a child thread")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        reply = False
        parent = None

        if 'parent' in validated_data:
            reply = True
            parent = validated_data["parent"]
            
        instance = News.objects.create(
            user=user,
            content=validated_data["content"],
            parent=parent,
            reply=reply
        )

        return instance


class NewsLikeOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = []

    def update(self, instance, validated_data):
        if self.context['request'].user in instance.liked.all():
            instance.liked.remove(self.context['request'].user)
        else:
            instance.liked.add(self.context['request'].user)

        instance.save()
        return instance

        