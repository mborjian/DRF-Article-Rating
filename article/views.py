from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Article, Rating
from .serializers import RatingSerializer, ArticleListSerializer


@login_required
def home(request):
    articles = Article.objects.order_by('-id')[:5]
    context = {'articles': articles}
    return render(request, 'article/home.html', context)


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer


class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
