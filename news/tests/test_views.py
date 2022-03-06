from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from news.models import News, Category


class NewsViewsTest(TestCase):

    def test_index(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'news/index.html')

    def test_show_category(self):

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

        response = self.client.get(reverse('category', args=('test',)))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'news/more.html')

    def test_hide(self):
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

        response = self.client.get(
            reverse('hide post', args=(1,)), follow=True)

        self.assertEqual(response.status_code, 200)

        news = News.objects.get(pk=1)

        self.assertFalse(news.is_published)

    def test_register_POST(self):

        response = self.client.post(reverse('register'),
                                    {
            'username': 'vasiliy',
            'password1': 'JSW3f6i-pcLgsKK',
            'password2': 'JSW3f6i-pcLgsKK',
        },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

    def test_register_GET(self):

        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'news/register.html')

    def test_autorize_GET(self):

        response = self.client.get(reverse('authorization'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'news/autorize.html')

    def test_autorize_POST(self):

        user = User.objects.create_user(
            'test_user',
            'wqfjodsjfWFHEOH23'
        )

        response = self.client.post(reverse('authorization'),
        {
            'username': 'test_user',
            'password': 'wqfjodsjfWFHEOH23',
        },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'news/autorize.html')

