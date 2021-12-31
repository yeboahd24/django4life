from django.db.models import Sum
from django.core.paginator import Paginator


from .filters import ArticleFilter


def common_data(request, queryset):
    data = {}
    data['last_articles'] = queryset.order_by('-date_published')[:3]
    data['popular_articles'] = queryset.annotate(
        Views=Sum('views')).order_by('-Views')[:3]
    return data


def filter_articles(request, queryset):
    data = {}
    articles_filter = ArticleFilter(request.GET, queryset=queryset)
    articles = articles_filter.qs
    data['articles_filter'] = articles_filter
    data['articles'] = articles
    return data


def obj_paginator(request, queryset):
    data = {}
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['page_obj'] = page_obj
    return data
