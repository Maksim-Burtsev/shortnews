from django import forms
from news.models import News
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm  

class SearchForm(forms.Form):
    """Поисковая строка на сайте"""
    
    query = forms.CharField(label='')
    widgets = {
        'query' : forms.TextInput(attrs={'name': 'q',
        'placeholder' : 'Search...'
        }),
    }

class UserAutorizeForm(AuthenticationForm):
    captcha = CaptchaField(label='')

class UserRegisterForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())
    captcha = CaptchaField(label='')
