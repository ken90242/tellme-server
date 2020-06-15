import django_filters
from django.db.models import Q

from .models import Question

class QuestionFilter(django_filters.rest_framework.FilterSet):
    has_answer = django_filters.BooleanFilter(label='has answer', method='answer_or_not')
    
    def answer_or_not(self, queryset, name, value):
        return queryset.filter(has_answer=value) if value else queryset

    class Meta:
        models = Question
        fields = ['has_answer']
