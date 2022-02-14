from django.shortcuts import redirect, render
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.core.cache import cache

from news.forms import SearchForm
from news.models import News, Category, Currency


def index(request):
    """Обратаывает главную страницу"""

    form = SearchForm()
    title = 'Главная страница'

    currs = cache.get('currs')
    if not currs:
        currs = Currency.objects.all()
        cache.set('currs', currs, 60)

    cats = Category.objects.prefetch_related('news_set').all()

    paginator = Paginator(cats, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    news_list = []

    for cat in page_obj.object_list:
        news_list.append(cat.news_set.filter(is_published=True)[:10])

    context = {
        'title': title,
        'form': form,
        'news_list': news_list,
        'page_obj': page_obj,
        'currency' : currs,
        'cats' : cats,
    }

    return render(request, 'news/index.html', context=context)


def show_category(request, cat_slug):
    """Выводит все посты конкретной категории на сайте"""

    title = get_object_or_404(Category, slug=cat_slug)
    curr = Currency.objects.all()

    if request.method == "POST":
        news_list = get_list_or_404(
            News, title__icontains=request.POST.get('query'), is_published=True)
        form = SearchForm(request.POST)
    else:
        news_list = get_list_or_404(News, cat_id=title.pk, is_published=True)
        form = SearchForm()

    context = {
        'title': title,
        'news_list': news_list,
        'form': form,
        'cat_slug': cat_slug,
        'currency' : curr,
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
                news_list = get_list_or_404(News, cat_id=cat.pk,is_published=True)
                flag = False
                break
        if flag:
            news_list = get_list_or_404(News, title__icontains=query, is_published=True)
        title = 'Результаты поиска'
        context = {
            'title': title,
            'news_list': news_list,
            'cats' : categories,
        }
        return render(request, 'news/search.html', context=context)
    else:
        raise ValidationError('Неправило заполненная форма!')

def hide(request, post_id):
    """Скрывает пост"""

    post = get_object_or_404(News, pk=post_id)
    post.is_published = False
    post.save()
    
    return redirect('home')