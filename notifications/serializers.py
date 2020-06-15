from rest_framework import serializers

from qa.models import Question
from articles.models import Article

class onlyUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        from users.models import User
        model = User
        fields = ['username']


class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        from news.models import News
        from .models import Notification
        valid_instance_types = (Article, Question, News)
        if isinstance(value, valid_instance_types):
            return str(value)

        raise Exception('Unexpected type(GenericForeignKey) for Notification object')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Notification
        model = Notification
        fields = ["unread"]

class NotificationDetailSerializer(serializers.ModelSerializer):
    action_object = ContentObjectRelatedField(read_only=True)
    verb = serializers.SerializerMethodField()
    actor = onlyUserNameSerializer()
    recipient = onlyUserNameSerializer()
    action_object_url = serializers.SerializerMethodField()

    class Meta:
        from .models import Notification
        model = Notification
        fields = "__all__"

    def get_action_object_url(self, obj):
        from news.models import News

        if isinstance(obj.action_object, Article):
            return '/{category}/{slug}'.format(
                category='article', slug=obj.action_object.slug)
        elif isinstance(obj.action_object, News):
            return '/{category}/{slug}'.format(
                category='news', slug=obj.action_object.uuid_id)
        elif isinstance(obj.action_object, Question):
            return '/{category}/{slug}'.format(
                category='qa', slug=obj.action_object.slug)
        return ''
    
    def get_verb(self, obj):
        return obj.get_verb_display()