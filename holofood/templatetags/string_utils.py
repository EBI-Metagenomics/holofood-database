from typing import List

from django import template

register = template.Library()


@register.filter(name="replace")
def replace(value: str, arg: str = "_> ") -> str:
    """
    Replace a substring with another.
    :param value: The string to be mutated.
    :param arg: A replacement of the form "oldtext>newtext". Note the importance of the >.
    :return: New string with replacement.
    """
    if arg.count(">") != 1:
        return value
    old, new = arg.split(">")
    return value.replace(old, new)
