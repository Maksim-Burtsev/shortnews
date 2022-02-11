from dataclasses import field
from re import A
from django import forms
from .models import News

class SearchForm(forms.Form):
    query = forms.CharField(label='')
    widgets = {
        'query' : forms.TextInput(attrs={'name': 'q',
        'placeholder' : 'Search...'
        }),
    }