import django_filters
from django.db.models import Q

from taggit.models import TaggedItem
from django.contrib.contenttypes.models import ContentType

class TaggedItemFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.CharFilter(label='Category', method='get_certain_category')

    def get_certain_category(self, queryset, name, value):
        return queryset.filter(content_type__model=value.lower()) if value else queryset
    
    class Meta:
        models = TaggedItem
        fields = ['category']

class TagFilter(django_filters.rest_framework.FilterSet):
    category = django_filters.CharFilter(label='Category', method='get_certain_category')

    def get_certain_category(self, queryset, name, value):
        return queryset.filter(content_type__model=value.lower()) if value else queryset
    
    class Meta:
        models = TaggedItem
        fields = ['category']
