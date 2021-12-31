from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import *
from .utils import common_data, filter_articles, obj_paginator
from .forms import GetEmailForm

# Create your views here.


def home(request):
    articles = Article.objects.all().order_by('-date_published')

    data = common_data(request, articles)
    last_articles = data['last_articles']
    popular_articles = data['popular_articles']

    filter = filter_articles(request, articles)
    articles_filter = filter['articles_filter']
    articles = filter['articles']

    paginator = obj_paginator(request, articles)
    page_obj = paginator['page_obj']

    template = render_to_string('core/email.html')
    if request.method == 'POST':
        if 'email' in request.POST:
            email_form = GetEmailForm(request.POST)
            if email_form.is_valid():
                user_eamil = email_form.cleaned_data['email']
                email = EmailMessage(
                    'Фишки Django',
                    template,
                    settings.EMAIL_HOST_USER,
                    [user_eamil]
                )
                email.fail_silently = False
                email.content_subtype = 'html'
                email.send()
                return redirect('email_sent')
    else:
        email_form = GetEmailForm()

    context = {
        'articles': articles,
        'last_articles': last_articles,
        'popular_articles': popular_articles,
        'page_obj': page_obj,
        'articles_filter': articles_filter,
        'email_form': email_form
    }
    return render(request, 'core/home.html', context)


def article(request, pk):
    article = Article.objects.get(title=pk)
    article.views = article.views + 1
    article.save()

    articles = Article.objects.all()
    data = common_data(request, articles)
    last_articles = data['last_articles']
    popular_articles = data['popular_articles']

    filter = filter_articles(request, articles)
    articles_filter = filter['articles_filter']
    articles = filter['articles']

    template = render_to_string('core/email.html')
    if request.method == 'POST':
        if 'email' in request.POST:
            email_form = GetEmailForm(request.POST)
            if email_form.is_valid():
                user_eamil = email_form.cleaned_data['email']
                email = EmailMessage(
                    ' Chips Django',
                    template,
                    settings.EMAIL_HOST_USER,
                    [user_eamil]
                )
                email.fail_silently = False
                email.content_subtype = 'html'
                email.send()
                return redirect('email_sent')
    else:
        email_form = GetEmailForm()

    # filter redirect
    if request.method == 'GET':
        if 'title' in request.GET:
            title = request.GET['title']
            request.path = request.META['HTTP_HOST']
            path = 'http://' + request.path + '/?title=' + title
            return redirect(path)

    last_article = Article.objects.all().order_by('-date_published')[0]

    context = {
        'article': article,
        'last_articles': last_articles,
        'popular_articles': popular_articles,
        'articles_filter': articles_filter,
        'last_article': last_article,
        'email_form': email_form
    }
    return render(request, 'core/article.html', context)


def tag_page(request, tag_title):
    tags = Tag.objects.filter(title=tag_title)
    articles = Article.objects.filter(tags__in=tags)

    articles_simple = Article.objects.all()
    data = common_data(request, articles_simple)
    last_articles = data['last_articles']
    popular_articles = data['popular_articles']

    filter = filter_articles(request, articles)
    articles_filter = filter['articles_filter']
    articles = filter['articles']

    paginator = obj_paginator(request, articles)
    page_obj = paginator['page_obj']

    template = render_to_string('core/email.html')
    if request.method == 'POST':
        if 'email' in request.POST:
            email_form = GetEmailForm(request.POST)
            if email_form.is_valid():
                user_eamil = email_form.cleaned_data['email']
                email = EmailMessage(
                    'Chips  Django',
                    template,
                    settings.EMAIL_HOST_USER,
                    [user_eamil]
                )
                email.fail_silently = False
                email.content_subtype = 'html'
                email.send()
                return redirect('email_sent')
    else:
        email_form = GetEmailForm()

    context = {
        'articles': articles,
        'last_articles': last_articles,
        'popular_articles': popular_articles,
        'page_obj': page_obj,
        'articles_filter': articles_filter,
        'email_form': email_form,
    }
    return render(request, 'core/home.html', context)


def email_sent(request):
    context = {}
    return render(request, 'core/email_sent.html', context)
