from django.contrib import admin

# Register your models here.

from app.models import Profile, ViewedProfiles,User

@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'bio', ]
    
@admin.register(ViewedProfiles)
class ViewedProfile(admin.ModelAdmin):
    list_display = ['user','profile',]
    
