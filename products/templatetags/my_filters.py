"""
Custom template tags and filters.
"""

from django import template

from products.views import SubcategoryIndex

register = template.Library()


@register.filter(name='times')
def times(number):
    """this filter used to return list of number to use in for loop."""

    return range(number)


@register.filter
def lookup(subcategory, key):
    """this filter used to return a value from subcategory."""

    if key >= SubcategoryIndex.index:
        SubcategoryIndex.index = key
    else:
        SubcategoryIndex.index += 1
    if len(subcategory[SubcategoryIndex.index]) == 2:
        return subcategory[SubcategoryIndex.index][1]
    return subcategory[SubcategoryIndex.index][2]


@register.filter
def lookup1(subcategory, key):
    """this filter used to return a list from subcategory."""

    if key >= SubcategoryIndex.index1:
        SubcategoryIndex.index1 = key
    else:
        SubcategoryIndex.index1 += 1
    return subcategory[SubcategoryIndex.index1]


@register.simple_tag
def define(value):
    """this tag used to change a value."""

    return value


@register.simple_tag
def get_id(value):

    print('value => ', value)
    return value
