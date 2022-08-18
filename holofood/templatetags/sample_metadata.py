from typing import Union, List

from django import template
from holofood.models import Sample, SampleStructuredDatum
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
    return f'{datum.measurement}{datum.units or ""}'


@register.inclusion_tag("holofood/components/data_type_icons.html", name="data_types")
def data_type_icons(sample: Sample) -> dict:
    if sample:
        return {
            "sample_metadata": (
                hasattr(sample, "primary_metadata") and len(sample.primary_metadata)
            )
            or sample.structured_metadata.exists(),
            "metagenomics": sample.has_metagenomics,
            "metabolomics": sample.has_metabolomics,
        }
    else:
        return {
            "sample_metadata": False,
            "metagenomics": False,
            "metabolomics": False,
        }


@register.filter(name="holofood_ordering_rules")
def order_metadata_by_holofood_rules(
    metadata: List[SampleStructuredDatum],
) -> List[SampleStructuredDatum]:
    def metadata_priority(metadatum: SampleStructuredDatum):
        marker_name_lower = metadatum.marker.name.lower()
        rules = (
            holofood_config.tables.metadata_list.bring_to_top_if_metadata_marker_name_contains
        )
        for idx, rule in enumerate(rules):
            if rule in marker_name_lower:
                return idx
        return len(rules) + 1

    return sorted(metadata, key=metadata_priority)
