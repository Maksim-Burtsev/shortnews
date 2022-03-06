from django.test import TestCase

from wiki.models import Article


class WikiModelTest(TestCase):

    def test_article(self):

        test_text = 'Тестовое содержание статьи. '*100

        article = Article.objects.create(
            title='Тестовый заголовок',
            summary=test_text,
            url='https://test.com',
        )

        self.assertEqual(article.title, 'Тестовый заголовок')
        self.assertEqual(article.summary, test_text)
        self.assertEqual(article.url, 'https://test.com')
        self.assertEqual(article.image_link, '')
        self.assertTrue(article.is_published)
