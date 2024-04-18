from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from account.forms import CustomUserCreationForm, LoginForm, UserUpdateForm
from article.models import Rating


class CustomRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('article.home')
    success_message = "You have successfully registered."

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field.capitalize()}: {error}')
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('article.home')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('article.home')

    def get_success_url(self):
        return self.success_url

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field.capitalize()}: {error}')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('article.home')
        return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account.login')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        response = super().dispatch(request, *args, **kwargs)
        if self.next_page:
            return redirect(self.next_page)
        else:
            return response


@login_required
def profile_view(request):
    user = request.user
    latest_ratings = Rating.objects.filter(user=user).order_by('-created')[:5]

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'form': form,
        'latest_ratings': latest_ratings
    }
    return render(request, 'account/profile.html', context)
