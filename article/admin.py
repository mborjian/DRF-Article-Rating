from django.contrib import admin

from article.models import Article, Rating


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)


class RatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rating, RatingAdmin)
