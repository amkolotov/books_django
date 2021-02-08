from django.contrib import admin

from .models import ContactUser


@admin.register(ContactUser)
class ContactUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')
