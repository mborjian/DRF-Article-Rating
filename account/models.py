from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return '{}'.format(self.username)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
