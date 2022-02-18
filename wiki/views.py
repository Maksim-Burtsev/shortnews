from msilib.schema import ListView
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import get_list_or_404

from wiki.models import Article


class WikiFeed(ListView):

    # paginate_by = 20
    model = Article
    template_name = 'wiki/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = get_list_or_404(Article, is_published=True)
        return articles

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['title'] = 'Случайные статьи'

def index(request):

    context = {
        'title' : 'Случайные статьи',
        'articles' : Article.objects.filter(is_published=True)
    }

    return render(request, 'wiki/index.html', context=context)