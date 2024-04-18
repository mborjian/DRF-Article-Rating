from rest_framework import serializers

from .models import Article, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'article', 'user', 'rating', 'created']


class ArticleListSerializer(serializers.ModelSerializer):
    rating_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'rating_count', 'average_rating', 'user_rating']

    def get_rating_count(self, obj):
        return Rating.objects.filter(article=obj).count()

    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(article=obj)
        if ratings.exists():
            return sum(rating.rating for rating in ratings) / ratings.count()
        return 0

    def get_user_rating(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            user_rating = Rating.objects.filter(article=obj, user=request.user).first()
            if user_rating:
                return user_rating.rating
        return None
