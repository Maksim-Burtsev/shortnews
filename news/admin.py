from django.contrib import admin
from news.models import Category, News

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):

    list_display = ('name', 'slug', 'link')
    prepopulated_fields = {'slug':('name', )}


admin.site.register(News)
