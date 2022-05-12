from typing import Union

from django import template
from django.forms import BoundField, Widget, Form
from django_filters.fields import ChoiceField, ChoiceIterator

register = template.Library()


@register.filter(name="with_classes")
def field_with_class(field: BoundField, classes: str) -> Widget:
    """
    Adds an HTML class to a django form field widget.

    Usage: {{ myform.myfield | with_classes:"my-class my-class__extra" }}

    :param field: The field instance of a django form.
    :param classes: A string of HTML class names.
    :return: Form field widget with classes appended.
    """
    new_class = field.css_classes(classes)
    return field.as_widget(attrs={"class": new_class})


@register.filter(name="contains_ordering_for")
def form_can_be_ordered_by(form: Form, param: str) -> bool:
    """
    Determine whether a queryset can be ordered by a certain parameter,
    by looking at whether a form contains an `ordering` field with the parameter as an option.
    This is compatible with the django_filters OrderingFilter.

    Usage: {% if form|contains_ordering_for:"accession" %}...

    :param form: Django form instance
    :param param: Name of the model field to order by
    :return: True if param is a valid ordering, else False.
    """
    ordering_field: Union[ChoiceField, None] = form.fields.get("ordering")
    if not ordering_field or not param:
        return False
    return param in map(lambda c: c[0], ordering_field.choices)
