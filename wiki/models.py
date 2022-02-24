from django.db import models


class Article(models.Model):
    """Статьи из википедии"""

    title = models.CharField('Заголовок', max_length=200)

    summary = models.TextField('Краткое содержание')

    url = models.URLField('Ссылка')

    image_link = models.CharField('Картинка', max_length=250, blank=True)

    is_published = models.BooleanField('Опубликовано', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'Статьи'
        ordering = ['?']        