from django.contrib import admin

from .models import Profile, Tweet, Following

admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Following)
