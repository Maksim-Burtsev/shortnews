from django import forms
from news.models import News
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    query = forms.CharField(label='')
    widgets = {
        'query' : forms.TextInput(attrs={'name': 'q',
        'placeholder' : 'Search...'
        }),
    }

# class RegisterUserForm(UserCreationForm):

#     class Meta:
#         model = User
#         widgets = {
#             'username' : forms.TextInput()
#         }
