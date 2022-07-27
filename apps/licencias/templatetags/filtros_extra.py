from atexit import register
from django import template

register = template.Library()

@register.filter(name='substract')
def substract(value, arg):
    return value - arg

