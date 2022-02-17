from turtle import mode
from django.db import models

# Create your models here.
class Article(models.Model):
    """Статьи из википедии"""    

    title = models.CharField('Заголовок', max_length=200)

    summary = models.TextField('Краткое содержание')

    url = models.URLField('Ссылка')

    image = models.ImageField('Фото', upload_to='wiki_photo', blank=True)

    is_published = models.BooleanField('Опубликовано', default=True)