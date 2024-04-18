from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    articles = Article.objects.order_by('-id')[:5]
    context = {'articles': articles}
    return render(request, 'article/home.html', context)

