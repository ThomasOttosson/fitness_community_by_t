from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


@register.filter
def round_int(value):
    try:
        return int(round(Decimal(value)))
    except (TypeError, InvalidOperation):
        return 0
