from django.test import TestCase
from django.contrib.auth.models import User

from news.forms import SearchForm, AuthenticationForm, UserRegisterForm


class NewsFormsTest(TestCase):

    def test_search_form(self):

        form = SearchForm(data={
            'query': 'test search text'
        })

        self.assertTrue(form.is_valid())
