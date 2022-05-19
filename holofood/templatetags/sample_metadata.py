import logging
from typing import Union, Dict

from django import template
from holofood.models import Sample
from holofood.utils import holofood_config

register = template.Library()


@register.filter(name="metadatum")
def metadatum(sample: Sample, marker_name: str) -> Union[str, None]:
    datum = None
    if (
        hasattr(sample, "primary_metadata")
        and marker_name
        in holofood_config.tables.samples_list.default_metadata_marker_columns
    ):
        try:
            datum = next(
                m for m in sample.primary_metadata if m.marker.name == marker_name
            )
        except StopIteration:
            # Metadata was prefetched but didn't exist on this sample
            pass
    else:
        # Metadata not prefetched
        datum = sample.structured_metadata.filter(marker__name=marker_name).first()

    if datum is None:
        return None
    logging.info(datum)
    return f'{datum.measurement}{datum.units or ""}'


@register.inclusion_tag("holofood/components/data_type_icons.html", name="data_types")
def data_type_icons(sample: Sample) -> Dict:
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
