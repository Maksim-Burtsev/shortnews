from django.contrib import admin
from django.urls import path, include
from news.views import *

urlpatterns = [
    # path('', NewsHome.as_view(), name='home'),
    path ('', index, name='home'),
    path('<slug:cat_slug>',show_category, name='category' ),
    path ('search/', search, name='search')
]