from django.shortcuts import render
from django.views.generic  import ListView, DetailView
from .models import News, Category

class NewsHome(ListView):
    """Класс, который выводит главную страницу."""

    model = News
    template_name = 'news/index.html'

    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.all()
        
        return context

    def get_queryset(self):
        items = []
        cats = Category.objects.prefetch_related('news_set').all()
        for cat in cats:
            # items.append(cat.news_set.select_related('cat')[:10])
            items.append(cat.news_set.all()[:10])

        return items
        # return News.objects.all()[:7]

class NewsCategory(ListView):
    """Класс, который выводит данные конкретной категории."""

    model = News
    template_name = 'news/more.html'

    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['cat_slug'])

        return context

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'])