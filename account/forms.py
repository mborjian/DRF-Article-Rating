from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(render_value=True),
    )

    password2 = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
