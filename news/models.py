from django.db import models
from django.urls import reverse

class News(models.Model):
    """Модель одной новости на сайте"""

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    
    link = models.CharField(max_length=200, verbose_name='Ссылка')
    
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'
        ordering = ['pk']

class Category(models.Model):
    """Каждая категория, или сайт, откуда парсятся данные"""

    name = models.CharField(max_length=200, verbose_name='Категория')
    
    slug = models.SlugField(max_length=200, unique=True, 
    
    verbose_name='Slug')    
    
    link = models.CharField(max_length=200, verbose_name='Ссылка')

    priority = models.IntegerField('Приоритет', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})
    

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['priority']

class Currency(models.Model):
    """Валюты"""

    name = models.CharField('Валюта', max_length=200)

    price = models.DecimalField('Стоимость', decimal_places=2, max_digits=10)

    time_updated = models.DateTimeField('Последнее обновление', auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'валюта'
        verbose_name_plural = 'Валюты'

        

