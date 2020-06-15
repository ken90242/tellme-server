from rest_framework import serializers

from django.db.models import Q
from .models import User
from upload.serializers import UserImageSerializer

class checkUserAuthSerializer(serializers.ModelSerializer):
    is_login_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'is_login_user']

    def get_is_login_user(self, obj):
        return obj.username == self.context['request'].user.username


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'picture', 'introduction', 'job_title', 'location']


class UserSerializer(serializers.ModelSerializer):
    moments_num = serializers.SerializerMethodField()
    article_num = serializers.SerializerMethodField()
    comment_num = serializers.SerializerMethodField()
    question_num = serializers.SerializerMethodField()
    answer_num = serializers.SerializerMethodField()
    interaction_num = serializers.SerializerMethodField()
    is_login_user = serializers.SerializerMethodField()
    picture = UserImageSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['is_login_user', 'comment_num', 'interaction_num', 'moments_num', 'article_num', 'question_num', 'answer_num', 'last_login', 'email', 'picture', 'introduction', 'job_title', 'location', 'username']
    
    def get_moments_num(self, obj):
        return obj.publisher.filter(reply=False).count()
    
    def get_is_login_user(self, obj):
        return obj.username == self.context['request'].user.username
    
    def get_article_num(self, obj):
        return obj.author.filter(status='P').count()
    
    def get_comment_num(self, obj):
        return obj.publisher.filter(reply=True).count() + obj.comment_comments.all().count()
    
    def get_question_num(self, obj):
        return obj.q_author.all().count()

    def get_answer_num(self, obj):
        return obj.a_author.all().count()
    
    def get_interaction_num(self, obj):
        return obj.liked_news.all().count() + obj.qa_vote.all().count()
    
