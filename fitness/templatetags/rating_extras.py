from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


# Template filter to round a given value to the nearest integer.
@register.filter
def round_int(value):
    try:
        return int(round(Decimal(value)))
    except (TypeError, InvalidOperation):
        return 0
