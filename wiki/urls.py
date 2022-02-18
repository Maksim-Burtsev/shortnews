from django.urls import path, include
from wiki.views import WikiFeed


urlpatterns = [
    path('', WikiFeed.as_view(), name='home1'),
]
