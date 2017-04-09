from django import template
from django.utils import timezone


register = template.Library()


@register.filter
def eligible(date):
    """Removes all values of arg from the given string"""
    now = timezone.now().date()
    delta_year = now.year - date.year
    if delta_year > 13:
        return 'allowed'
    elif delta_year == 13 and now.day > date.day and now.month >= date.month:
        return 'allowed'
    return 'blocked'


@register.filter
def fizzbuzz(num):
    msg = ''
    if num % 3 == 0:
        msg += 'Fizz'
    if num % 5 == 0:  # no more elif
        msg += 'Buzz'
    if not msg:  # check if msg is an empty string
        msg += str(num)
    return msg
