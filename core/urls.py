from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('article/<str:pk>', views.article, name="article"),
    path('tag/?:<str:tag_title>/', views.tag_page, name="tag"),
    path('email_sent/', views.email_sent, name="email_sent")
]
