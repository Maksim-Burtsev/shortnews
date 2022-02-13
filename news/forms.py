from django import forms
from news.models import News

class SearchForm(forms.Form):
    query = forms.CharField(label='')
    widgets = {
        'query' : forms.TextInput(attrs={'name': 'q',
        'placeholder' : 'Search...'
        }),
    }