from django.urls import path

from article.views import home

urlpatterns = [
    path('', home, name='article.home'),
]
