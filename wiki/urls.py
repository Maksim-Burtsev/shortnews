from django.urls import path, include
from wiki.views import index

urlpatterns = [
    path ('', index, name='home'),
]