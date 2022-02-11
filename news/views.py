from django.shortcuts import redirect, render
from django.views.generic  import ListView, DetailView
from .models import News, Category
from .forms import SearchForm
from django.http import Http404
from django.shortcuts import get_list_or_404

def index(request):
    
    form = SearchForm()
    title = 'Главная страница'

    news_list = []
    cats = Category.objects.prefetch_related('news_set').all()
    for cat in cats:
        news_list.append(cat.news_set.all()[:10])

    context = {
        'title' : title,
        'form' : form,
        'news_list' : news_list,
    }
    
    return render(request, 'news/index.html', context=context)

def show_category(request, cat_slug):

    title = Category.objects.get(slug=cat_slug)

    news_list = News.objects.filter(cat_id=title.pk)

    context = {
        'title' : title,
        'news_list' : news_list,
    }

    return render(request, 'news/more.html', context=context)

def search(request):
    query = request.GET.get('query') 
    form = SearchForm(request.GET)
    if form.is_valid():
        categories = Category.objects.all()
        flag = True
        for cat in categories:
            if query.lower() == cat.name.lower():
                news_list = News.objects.filter(cat_id=cat.pk)
                flag = False
                break
        if flag:
            news_list = get_list_or_404(News, title__icontains=query)
        title = 'Результаты поиска'
        context = {
            'title' : title,
            'news_list' : news_list,
        }
        return render(request, 'news/search.html', context=context)
    else:
        raise Http404

# class NewsHome(ListView):
#     """Класс, который выводит главную страницу."""

#     model = News
#     template_name = 'news/index.html'
#     form_class = TestForm
#     context_object_name = 'news_list'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Главная страница'
#         context['categories'] = Category.objects.all()
        
#         return context

#     def get_queryset(self):
#         items = []
#         cats = Category.objects.prefetch_related('news_set').all()
#         for cat in cats:
#             # items.append(cat.news_set.select_related('cat')[:10])
#             items.append(cat.news_set.all()[:10])

#         return items
#         # return News.objects.all()[:7]

# class NewsCategory(ListView):
#     """Класс, который выводит данные конкретной категории."""

#     model = News
#     template_name = 'news/more.html'

#     context_object_name = 'news_list'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = Category.objects.get(slug=self.kwargs['cat_slug'])

#         return context

#     def get_queryset(self):
#         return News.objects.filter(cat__slug=self.kwargs['cat_slug'])
