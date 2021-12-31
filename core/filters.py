import django_filters
from django_filters import CharFilter
from django.forms.widgets import TextInput

from .models import *


class ArticleFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains',
                       label='', widget=TextInput(attrs={'placeholder': ' Search  ...'}))

    class Meta:
        model = Article
        fields = ['title']
