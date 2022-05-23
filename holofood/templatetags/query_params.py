from django import template

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
