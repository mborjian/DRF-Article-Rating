from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    # App-specific URL patterns
    path('', include('article.urls')),
    path('a/', include('account.urls')),
]

# Serve static and media files in development
urlpatterns += staticfiles_urlpatterns()
