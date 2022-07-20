from django import template

register = template.Library()


@register.inclusion_tag("holofood/components/atoms/taxonomy_tooltip.html")
def taxonomy_tooltip(taxonomy: str, separator: str = ">", default: str = "—") -> dict:
    if taxonomy is None or separator not in taxonomy:
        return {"short_tax": default, "long_tax": None}
    return {"short_tax": taxonomy.split(separator)[-1].strip(), "long_tax": taxonomy}
