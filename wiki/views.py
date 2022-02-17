from msilib.schema import ListView
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import get_list_or_404

from wiki.models import Article


class WikiFeed(ListView):
    model = Article
    template_name = 'wiki/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = get_list_or_404(Article, is_published=True)
        return articles
