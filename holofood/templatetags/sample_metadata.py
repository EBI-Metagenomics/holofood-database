from typing import Union

from django import template
from holofood.models import Sample

register = template.Library()


@register.filter(name="metadatum")
def metadatum(sample: Sample, marker_name: str) -> Union[str, None]:
    # TODO move to manager and config file for default columns (to make use of prefetch)
    datum = sample.structured_metadata.filter(marker__name=marker_name).first()
    if datum is None:
        return None

    return f'{datum.measurement}{datum.units or ""}'


@register.inclusion_tag("holofood/components/data_type_icons.html", name="data_types")
def data_type_icons(sample: Sample) -> dict:
    if sample:
        return {
            "sample_metadata": True,
            "metagenomics": True,
            "metabolomics": True,
            "mags": True,
        }
    else:
        return {
            "sample_metadata": False,
            "metagenomics": False,
            "metabolomics": False,
            "mags": False,
        }
