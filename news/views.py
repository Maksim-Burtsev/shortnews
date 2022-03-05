from django.shortcuts import redirect, render
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Prefetch, OuterRef, Subquery


from news.forms import SearchForm, UserAutorizeForm, UserRegisterForm
from news.models import News, Category, Currency
from news.parsers.activate import update_db


def index(request):
    """Обратаывает главную страницу"""

    if request.method == "POST" and request.user.is_superuser:
        if request.POST.get('update'):
            update_db()

    form = SearchForm()

    currs = cache.get('currs')
    if not currs:
        currs = Currency.objects.all()
        cache.set('currs', currs, 60)

    subquery = Subquery(News.objects.filter(cat_id=OuterRef(
        'cat_id'), is_published=True).values_list("id", flat=True)[:10])

    cats = Category.objects.prefetch_related(
        Prefetch('news_set', queryset=News.objects.filter(id__in=subquery)))

    paginator = Paginator(cats, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Галавная страница',
        'form': form,
        'page_obj': page_obj,
        'currency': currs,
        'cats': cats,
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
        'currency': curr,
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
                news_list = get_list_or_404(
                    News, cat_id=cat.pk, is_published=True)
                flag = False
                break
        if flag:
            news_list = get_list_or_404(
                News, title__icontains=query, is_published=True)
        title = 'Результаты поиска'
        context = {
            'title': title,
            'news_list': news_list,
            'cats': categories,
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


def register(request):
    """Обрабатывает страницу регистрации пользователя"""

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('home')

    form = UserRegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }

    return render(request, 'news/register.html', context=context)


def authorization(request):
    """Обрабатывает страницу авторизации пользователя"""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('authorization')

    form = UserAutorizeForm()
    context = {
        'title': 'Авторизация',
        'form': form,
    }

    return render(request, 'news/autorize.html', context=context)


def logout_user(request):
    """Выход из учётной записи"""

    logout(request)
    return redirect('home')
