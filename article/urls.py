from django.urls import path

from article.views import home, rate_article_view, article_detail_view

urlpatterns = [
    path('', home, name='article.home'),
    path('article/<int:article_id>/', article_detail_view, name='article_detail'),
    path('article/<int:article_id>/rate/', rate_article_view, name='rate_article'),
]
