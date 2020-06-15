import django_filters
from django.db.models import Q

from .models import Notification

class NotificationFilter(django_filters.rest_framework.FilterSet):
    # pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    # pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    # top_category = django_filters.NumberFilter(method='top_category_filter')
    # is_new = django_filters.BooleanFilter(field_name='is_new', lookup_expr='exact')
    # is_hot = django_filters.BooleanFilter(field_name='is_hot', lookup_expr='exact')
    top_five = django_filters.BooleanFilter(label='Recent five notifications', method='recent_notifications')
    unread = django_filters.BooleanFilter(label='Unread notifications', method='has_not_been_read')

    def recent_notifications(self, queryset, name, value):
        return queryset[:5] if value else queryset

    def has_not_been_read(self, queryset, name, value):
        return queryset.filter(unread=True) if value else queryset
    
    class Meta:
        models = Notification
        fields = ['unread', 'top_five']
