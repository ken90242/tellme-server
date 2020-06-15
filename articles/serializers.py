import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from django.db.models import Q
from markdownx.utils import markdownify
from django.contrib.auth import get_user_model
from django_comments.models import Comment
from markdownx.utils import markdownify
from taggit.models import TaggedItem, Tag

from tellme.settings import SITE_ID
from users.serializers import UserSerializer
from upload.serializers import ArticleImageSerializer
from .models import Article

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    def get_count(self, obj):
        result = TaggedItem.objects.filter(tag_id=obj.id)

        if 'category' in self.context['request'].query_params:
            model_name = self.context['request'].query_params['category'].lower()
            result = result.filter(content_type__model=model_name)
        return result.count()

    class Meta:
        model = Tag
        fields = ['name', 'count']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article_slug = serializers.CharField(required=True, max_length=80, write_only=True)
    markdown_content = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = ["comment", "user", "markdown_content", "article_slug"]
        ordering = ["-submit_date"]
    
    def get_markdown_content(self, obj):
        return markdownify(obj.comment)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['site_id'] = SITE_ID
        attrs["content_type_id"] = 9

        article_instance = Article.objects.filter(slug=attrs.pop('article_slug'))
        if not article_instance:
            raise ValidationError("Unknown slug which does not fit any existing articles")

        attrs["object_pk"] = article_instance[0].id

        return attrs

class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = Article
        fields = ["image", "title", "content", "tags", "status", "edited", "comments"]


class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    image = ArticleImageSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        # lookup_field = "slug"

