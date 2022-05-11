import logging

from django import template
from django.forms import BoundField, Widget

register = template.Library()


@register.filter(name="with_classes")
def field_with_class(field: BoundField, classes: str) -> Widget:
    new_class = field.css_classes(classes)
    return field.as_widget(attrs={"class": new_class})
