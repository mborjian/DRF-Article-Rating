from django.contrib import admin

from account.models import User


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, AccountAdmin)
