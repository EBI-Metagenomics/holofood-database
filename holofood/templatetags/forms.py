from typing import Union

from django import template
from django.forms import BoundField, Widget, Form
from django_filters.fields import ChoiceField, ChoiceIterator

register = template.Library()


@register.filter(name="with_classes")
def field_with_class(field: BoundField, classes: str) -> Widget:
    new_class = field.css_classes(classes)
    return field.as_widget(attrs={"class": new_class})


@register.filter(name="contains_ordering_for")
def form_can_be_ordered_by(form: Form, param: str) -> bool:
    ordering_field: Union[ChoiceField, None] = form.fields.get("ordering")
    if not ordering_field or not param:
        return False
    return param in map(lambda c: c[0], ordering_field.choices)
