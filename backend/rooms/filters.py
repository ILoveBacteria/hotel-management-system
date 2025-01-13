import django_filters
from rooms.models import RoomType

class RoomTypeFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = RoomType
        fields = ['min_price', 'max_price', 'double_beds', 'single_beds']
        