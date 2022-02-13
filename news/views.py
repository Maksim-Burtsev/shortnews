from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator

from news.forms import SearchForm
from news.models import News, Category


def index(request):
    """Обратаывает главную страницу"""

    form = SearchForm()
    title = 'Главная страница'

    cats = Category.objects.prefetch_related('news_set').all()
    
    paginator = Paginator(cats, 2)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    news_list = []

    for cat in page.object_list:
        news_list.append(cat.news_set.all()[:10])

    context = {
        'title': title,
        'form': form,
        'news_list': news_list,
    }

    return render(request, 'news/index.html', context=context)


def show_category(request, cat_slug):
    """Выводит все посты конкретной категории на сайте"""

    title = get_object_or_404(Category, slug=cat_slug)

    if request.method == "POST":
        news_list = get_list_or_404(
            News, title__icontains=request.POST.get('query'))
        form = SearchForm(request.POST)
    else:
        news_list = get_list_or_404(News, cat_id=title.pk)
        # news_list = News.objects.filter(cat_id=title.pk)
        form = SearchForm()

    context = {
        'title': title,
        'news_list': news_list,
        'form': form,
        'cat_slug': cat_slug,
    }

    return render(request, 'news/more.html', context=context)


def search(request):
    """Выводит результаты поиска"""

    query = request.GET.get('query')
    form = SearchForm(request.GET)
    if form.is_valid():
        categories = Category.objects.all()
        flag = True
        for cat in categories:
            if query.lower() == cat.name.lower():
                news_list = get_list_or_404(News, cat_id=cat.pk)
                flag = False
                break
        if flag:
            news_list = get_list_or_404(News, title__icontains=query)
        title = 'Результаты поиска'
        context = {
            'title': title,
            'news_list': news_list,
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
