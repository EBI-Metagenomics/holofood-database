from typing import List

from django import template

register = template.Library()


@register.filter(name="split_by")
def split_by(value: str, arg: str = ",") -> List[str]:
    return value.split(arg)
