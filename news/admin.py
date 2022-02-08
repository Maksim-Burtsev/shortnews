from django.contrib import admin
from .models import Category, News

class AdminCategory(admin.ModelAdmin):

    list_display = ('name', 'slug', 'link')
    prepopulated_fields = {'slug':('name', )}


admin.site.register(News)
admin.site.register(Category, AdminCategory)
