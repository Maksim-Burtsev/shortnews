from django.test import TestCase
from django.urls import reverse

from wiki.models import Article


class WikiViewsTest(TestCase):

    def test_wiki_feed(self):

        test_text = 'Тестовое содержание статьи. '*100

        for i in range(100):
            article = Article.objects.create(
                title=f'Тестовый заголовок{i}',
                summary=f'{test_text} {i}',
                url=f'https://test{i}.com',
            )

        response = self.client.get(
            reverse('wiki:home'),
            {'page': '5'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'wiki/index.html')

        self.assertEqual(str(response.context_data['page_obj']),'<Page 5 of 5>')

        self.assertEqual(len(response.context_data['object_list']), 20)

    def test_wrong_wiki_page(self):

        test_text = 'Тестовое содержание статьи. '*100

        for i in range(100):
            article = Article.objects.create(
                title=f'Тестовый заголовок{i}',
                summary=f'{test_text} {i}',
                url=f'https://test{i}.com',
            )

        response = self.client.get(
            reverse('wiki:home'),
            {'page': '7'}
        )

        self.assertEqual(response.status_code, 404)