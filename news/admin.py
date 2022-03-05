from lib2to3.pgen2.token import CIRCUMFLEXEQUAL
from django.contrib import admin

from news.models import Category, News, Currency


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):

    list_display = ('name', 'slug', 'link')
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(News)
admin.site.register(Currency)
