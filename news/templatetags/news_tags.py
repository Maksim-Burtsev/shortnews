from django import template

from news.views import register


register = template.Library()

@register.filter
def index(indexble, i):
    return indexble[i]