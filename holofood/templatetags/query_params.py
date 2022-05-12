from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_for_param(context, **kwargs):
    """
    Constructs a URL that switches a single query parameter for another.
    Useful for changing e.g. ?page= in a GET that already includes things like a filter state e.g. ?type=chicken.

    Usage: <a href="{% url_for_param page=3 %}">3</a>

    :param context: Django context is needed for the Request.
    :param kwargs: Dict of query params and values to replace.
    :return: URL-encoded string with new query params.
    """
    to = context["request"].GET.copy()
    for qp, new_val in kwargs.items():
        to[qp] = new_val

    return f"?{to.urlencode()}"
