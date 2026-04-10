import django_filters
from .models import Movie


class MovieFilter(django_filters.FilterSet):
    release_year_min = django_filters.NumberFilter(field_name='release_year', lookup_expr='gte')
    release_year_max = django_filters.NumberFilter(field_name='release_year', lookup_expr='lte')
    rating_min = django_filters.NumberFilter(field_name='avg_rating', lookup_expr='gte')
    runtime_max = django_filters.NumberFilter(field_name='runtime_minutes', lookup_expr='lte')
    genre = django_filters.CharFilter(field_name='genres__slug', lookup_expr='exact')
    language = django_filters.CharFilter(field_name='language', lookup_expr='iexact')
    content_rating = django_filters.CharFilter(field_name='content_rating', lookup_expr='exact')

    class Meta:
        model = Movie
        fields = [
            'release_year_min', 'release_year_max', 'rating_min',
            'runtime_max', 'genre', 'language', 'content_rating', 'is_featured',
        ]
