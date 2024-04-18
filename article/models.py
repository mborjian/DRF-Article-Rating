from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(6)])

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user.username}'s rating for {self.article.title}"
