from django import template
from django.template.defaultfilters import stringfilter
import math

register = template.Library()

@register.filter
def millennium(value):
    if str(value).startswith('-'):
        value = str(value)[1:]
        value = math.ceil(float(value) / 1000)
        return value*-1
    else:
        return math.ceil(float(value)/1000)