from django.urls import path
from wiki.views import WikiFeed

app_name = 'wiki'
urlpatterns = [
    path('', WikiFeed.as_view(), name='home'),
]
