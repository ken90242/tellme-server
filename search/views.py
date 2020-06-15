from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet
from haystack.query import SearchQuerySet, EmptySearchQuerySet

from .search_indexes import ArticleIndex, NewsIndex, QuestionIndex, UserIndex, TagsIndex  # BYOI™ (Bring Your Own Index)
from news.models import News
from news.serializers import NewsDetailSerializer
from articles.models import Article
from articles.serializers import ArticleDetailSerializer
from qa.models import Question, Answer
from qa.serializers import QuestionDetailSerializer
from django.contrib.auth import get_user_model
from taggit.models import Tag
from users.serializers import UserSerializer

from rest_framework import serializers
from rest_framework import mixins
from rest_framework import viewsets

User = get_user_model()


class NewsSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = NewsDetailSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptySearchQuerySet()

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            sub = SearchQuerySet().models(News).filter(text__contains=query).values_list('uuid_id', flat=True)
            queryset = News.objects.filter(uuid_id__in=sub)

        return queryset


class QuestionSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionDetailSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptySearchQuerySet()

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            sub = SearchQuerySet().models(Question).filter(text__contains=query).values_list('slug', flat=True)
            queryset = Question.objects.filter(slug__in=sub)

        return queryset


class UserSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptySearchQuerySet()

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            sub = SearchQuerySet().models(User).filter(text__contains=query).values_list('username', flat=True)
            queryset = User.objects.filter(username__in=sub)

        return queryset


class ArticleSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ArticleDetailSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptySearchQuerySet()

        if request.GET.get('q') is not None:
            query = request.GET.get('q')
            sub = SearchQuerySet().models(Article).filter(text__icontains=query).values_list('slug', flat=True)
            queryset = Article.objects.filter(slug__in=sub)

        return queryset

