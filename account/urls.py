from django.urls import path

from account.views import CustomRegisterView, CustomLoginView, CustomLogoutView, profile_view

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='account.register'),
    path('login/', CustomLoginView.as_view(), name='account.login'),
    path('logout/', CustomLogoutView.as_view(), name='account.logout'),

    path('profile/', profile_view, name='account.profile'),
]
