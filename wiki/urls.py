from django.urls import path, include
from wiki.views import WikiFeed, index


urlpatterns = [
    path('', WikiFeed.as_view(), name='home1'),
]
