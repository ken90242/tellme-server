from django.utils import timezone
from haystack import indexes

from news.models import News
from articles.models import Article
from qa.models import Question, Answer
from django.contrib.auth import get_user_model
from taggit.models import Tag

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """對Article中的部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/articles_text.txt')
    title = indexes.CharField(model_attr="title")
    slug = indexes.CharField(model_attr="slug")
    content = indexes.CharField(model_attr="content")

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status="P", updated_at__lte=timezone.now())


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    """對News中的部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/news_text.txt')
    content = indexes.CharField(model_attr="content")
    uuid_id = indexes.CharField(model_attr="uuid_id")

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(reply=False, updated_at__lte=timezone.now())


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    """对Question模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/questions_text.txt')
    title = indexes.CharField(model_attr="title")
    content = indexes.CharField(model_attr="content")
    slug = indexes.CharField(model_attr="slug")

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=timezone.now())


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    """对User模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/users_text.txt')
    username = indexes.CharField(model_attr="username")
    nickname = indexes.CharField(model_attr="nickname", null=True)

    def get_model(self):
        return get_user_model()

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=timezone.now())


class TagsIndex(indexes.SearchIndex, indexes.Indexable):
    """对Tags模型类中部分字段建立索引"""
    text = indexes.CharField(document=True, use_template=True, template_name='search/tags_text.txt')
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Tag

    def index_queryset(self, using=None):
        return self.get_model().objects.all()