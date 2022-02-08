from django.shortcuts import render
from django.views.generic  import ListView, DetailView
from .models import News, Category

class NewsHome(ListView):

    model = News
    template_name = 'news/index.html'

    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.all()
        
        return context

    def get_queryset(self):
        return News.objects.all()[:7]

class NewsCategory(ListView):

    model = News
    template_name = 'news/more.html'

    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['cat_slug'])

        return context

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'])