from django.contrib import admin

# Register your models here.

from app.models import Profile

@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'bio']  