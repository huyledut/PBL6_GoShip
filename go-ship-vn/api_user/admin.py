from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", 'phone_number', 'last_name', 'first_name')


admin.site.register(models.User, UserAdmin)