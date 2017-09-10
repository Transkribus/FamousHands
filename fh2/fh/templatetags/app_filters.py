'''
Created on Jun 20, 2017

@author: albert
'''

from django import template
import math
#from datetime import date, timedelta

register = template.Library()

@register.filter(name='get_type')

def get_type(value):
    return str(type(value))

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    
    if not key in dict_data:
        return ""
    
    if key:
        return dict_data.get(key)
    


@register.filter
def millennium(value):
    if str(value).startswith('-'):
        value = str(value)[1:]
        value = math.ceil(float(value) / 1000)
        return value*-1
    elif value == None:
        return value
    else:
        value = str(value)
        return math.ceil(float(value)/1000)

@register.filter(name='century')
def century(value):
    if str(value).startswith('-'):
        value = str(value)[1:]
        value = math.ceil(float(value) / 100)
        return value*-1
    elif value == None:
        return value
    else:
        value = str(value)
        return math.ceil(float(value)/100)
    
@register.filter(name='decade')
def decade(value):
    if str(value).startswith('-'):
        value = str(value)[1:]
        value = math.floor(float(value) / 10)
        return value*-1
    elif value == None:
        return value
    else:
        value = str(value)
        return math.floor(float(value)/10)