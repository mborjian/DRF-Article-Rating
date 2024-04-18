from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Article, Rating
from .serializers import RatingSerializer, ArticleListSerializer


def home(request):
    articles = Article.objects.annotate(
        rating_count=Count('rating', distinct=True),
        average_rating=Avg('rating__rating')
    ).order_by('id')

    if request.user.is_authenticated:
        user_ratings = {rating.article_id: rating for rating in Rating.objects.filter(user=request.user)}
        for article in articles:
            article.user_rating = user_ratings.get(article.id)

    context = {'articles': articles}
    return render(request, 'article/home.html', context)


@login_required
def rate_article_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))
        if 0 <= rating_value <= 5:
            try:
                rating = Rating.objects.get(user=request.user, article=article)
                rating.rating = rating_value
            except Rating.DoesNotExist:
                rating = Rating(user=request.user, article=article, rating=rating_value)

            rating.save()

    return redirect('article_detail', article_id=article_id)


def article_detail_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, article=article).first()

    average_rating = Rating.objects.filter(article=article).aggregate(Avg('rating'))['rating__avg']

    context = {'article': article, 'user_rating': user_rating, 'average_rating': average_rating}
    return render(request, 'article/article_detail.html', context)


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
