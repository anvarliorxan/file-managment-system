import django_filters
from .models import File

class FileFilter(django_filters.FilterSet):
    hashtag = django_filters.CharFilter(field_name='hashtags__name', label='Hashtag Name')

    class Meta:
        model = File
        fields = ['hashtag']