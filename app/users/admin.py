from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'api_tomtom']
admin.site.register(Profile, ProfileAdmin)