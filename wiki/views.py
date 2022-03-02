from msilib.schema import ListView
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.core.cache import cache
from django.shortcuts import get_list_or_404


from wiki.models import Article
from wiki.parser.wiki import update_wiki_db


class WikiFeed(ListView):

    paginate_by = 20
    model = Article
    template_name = 'wiki/index.html'
    context_object_name = 'articles'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Случайные статьи'
        return context

    def get_queryset(self):
        
        articles = cache.get('articles')
        if not articles:
            articles = get_list_or_404(
                Article, is_published=True
                )
            cache.set('articles', articles)
            
        return articles

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            update_wiki_db()

        return redirect('wiki:home')
