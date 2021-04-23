from django.contrib import admin
from user.models import UserProfile,Profile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','address','phone','city','country','image_tag']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Profile)