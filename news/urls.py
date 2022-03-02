from django.contrib import admin
from django.urls import path, include
from news.views import *


urlpatterns = [
    path ('', index, name='home'),
    path('<slug:cat_slug>',show_category, name='category' ),
    path ('search/', search, name='search'),
    path('hide/<int:post_id>', hide, name='hide post'),
    path('register/', register, name='register'),
    path ('authorization/', authorization, name='authorization'),
    path ('logout/', logout_user, name='logout'),
]