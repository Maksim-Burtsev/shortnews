from django.contrib import admin
from django.urls import path, include
from .views import NewsHome, NewsCategory

urlpatterns = [
    path('', NewsHome.as_view(), name='home'),
    path('<slug:cat_slug>', NewsCategory.as_view(), name='category' )
]