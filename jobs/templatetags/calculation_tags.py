# jobs/templatetags/calculation_tags.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Ko'paytirish filtri"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Bo'lish filtri"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0