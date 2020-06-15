from django.shortcuts import render

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from markdownx.utils import markdownify
from django.db.models import Q
from django.views.generic.base import View
from django.http import JsonResponse
from django.http import Http404
from django_comments.models import Comment
from django_comments.signals import comment_was_posted
from notifications.views import notification_handler
from rest_framework import permissions

from .models import Article
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer, TagSerializer
from .filters import TaggedItemFilter
from markdownx.utils import markdownify
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from taggit.models import TaggedItem, Tag

class TagViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # filter_class = TaggedItemFilter


class ArticleViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Article.objects.filter(status='P')
    lookup_field = 'slug'
    authentication_classes = (JSONWebTokenAuthentication,)
    
    # [permissions.IsAuthenticated()]
    def get_permissions(self):
        return []

    def get_serializer_class(self):
        if self.action == "update":
            return ArticleSerializer
        return ArticleDetailSerializer


class CommentViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True, context={ 'request': self.request })
        for idx, instance in enumerate(serializer.data):
            serializer.data[idx]['comment'] = markdownify(instance['comment'])
        return Response(serializer.data)

    def perform_create(self, serializer):
        """文章有評論時通知作者"""
        comment = serializer.save(user=self.request.user)
        actor = self.request.user
        obj = comment.content_object
        notification_handler(actor, obj.user, 'C', obj, id_value=obj.slug)


class DraftViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    # def create(self, request, *args, **kwargs):
    #     print(request.POST)
    def get_queryset(self):
        queryset = Article.objects.filter(status='D', user=self.request.user)
        return queryset
    
    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleDetailSerializer
        if self.action == "update" or self.action == "create":
            return ArticleSerializer

        return ArticleDetailSerializer


class MarkdonViewset(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return JsonResponse({"result": markdownify(request.POST.get('content', ""))})
