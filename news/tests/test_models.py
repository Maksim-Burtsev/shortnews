from django.test import TestCase
from django.urls import reverse

from news.models import News, Category, Currency


class NewsModelsTest(TestCase):

    def test_news(self):

        cat = Category.objects.create(
            name='Тестовая категория',
            slug='test',
            link='https://test_link.com',
        )
        for _ in range(10):
            news = News.objects.create(
                title='Тестовая новость',
                link='https://google.com',
                cat_id=1,
            )

        one_news = News.objects.get(pk=1)
        all_news = News.objects.all()

        self.assertEqual(one_news.title, 'Тестовая новость')

        self.assertEqual(one_news.link, 'https://google.com')

        self.assertTrue(one_news.is_published)

        self.assertEqual(one_news.cat.name, 'Тестовая категория')

        self.assertEqual(str(one_news), 'Тестовая новость')

        self.assertEqual(all_news.count(), 10)

    def test_caregory(self):
        cat = Category.objects.create(
            name='Тестовая категория',
            slug='test',
            link='https://test_link.com',
            priority=10,
        )

        self.assertEqual(cat.name, 'Тестовая категория')

        self.assertEqual(cat.slug, 'test')
        
        self.assertEqual(cat.link, 'https://test_link.com')
        
        self.assertEqual(cat.priority, 10)
        
        self.assertTrue(cat.is_puslished)

        self.assertEqual(str(cat), 'Тестовая категория')


    def test_currency(self):
        
        curr = Currency.objects.create(
            name = '₣',
            price = 12.34,
        )

        self.assertEqual(curr.name, '₣')

        self.assertEqual(float, type(curr.price))

        self.assertEqual(str(curr), '₣')
