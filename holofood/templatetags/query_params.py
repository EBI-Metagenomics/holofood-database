from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def url_for_params(context, **kwargs):
    """
    Constructs a URL that switches multiple query parameter for new values.
    Useful for changing e.g. ?page= in a GET that already includes things like a filter state e.g. ?type=chicken.

    Usage: <a href="{% url_for_params page=3 %}">3</a>

    :param context: Django context is needed for the Request.
    :param kwargs: Dict of query params and values to replace.
    :return: URL-encoded string with new query params.
    """
    to = context["request"].GET.copy()
    for qp, new_val in kwargs.items():
        to[qp] = new_val

    return f"?{to.urlencode()}"


@register.simple_tag(takes_context=True)
def url_for_param(context, param, value):
    """
    Constructs a URL that switches a single query parameter for another.
    Useful for changing e.g. ?related_field_page= in a GET that already includes things like
    a filter state e.g. ?type=chicken, and where the param itself is variable (i.e. not always called "page").

    Usage: <a href="{% url_for_params param='related_field_page' value=3 %}">3</a>

    :param value: New value for query param
    :param param: String name of query param
    :param context: Django context is needed for the Request.
    :return: URL-encoded string with new query params.
    """
    to = context["request"].GET.copy()
    to[param] = value

    return f"?{to.urlencode()}"


@register.simple_tag(takes_context=True)
def url_preserving_params(context, viewname, **kwargs):
    """
    Construct a URL for view_name whilst preserving the current URL Query Parameters.

    Usage:  <a href="{% url_preserving_params 'viral_catalogue_fragment' pk=catalogue.id %}">3</a>

    :param context: Django template context
    :param viewname: The Django URL pattern name to be reversed.
    :param kwargs: Dict of arguments for the URL.
    :return: URL string.
    """
    base_url = reverse(viewname, kwargs=kwargs)
    return f'{base_url}?{context["request"].GET.copy().urlencode()}'


@register.inclusion_tag(
    "holofood/components/atoms/clear_filters.html", takes_context=True
)
def clear_filters_button(context):
    request = context["request"]
    return {
        "has_query_params": len(request.GET) > 0,
        "url": request.build_absolute_uri(request.path),
    }
