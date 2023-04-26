from typing import Union, List

from django import template
from holofood.models import Sample, SampleStructuredDatum, Animal
from holofood.utils import holofood_config

register = template.Library()


@register.filter(name="animal_metadatum")
def animal_metadatum(animal: Animal, marker_name: str) -> Union[str, None]:
    primary_marker_list = (
        holofood_config.tables.animals_list.default_metadata_marker_columns
    )
    datum = None
    if hasattr(animal, "primary_metadata") and marker_name in primary_marker_list:
        try:
            datum = next(
                m for m in animal.primary_metadata if m.marker.name == marker_name
            )
        except StopIteration:
            # Metadata was prefetched but didn't exist on this sample
            pass
    else:
        # Metadata not prefetched
        datum = animal.structured_metadata.filter(marker__name=marker_name).first()

    if datum is None:
        return None
    measurement_includes_units = str(datum.measurement).endswith(str(datum.units))
    return f'{datum.measurement}{datum.units if datum.units and not measurement_includes_units else ""}'


@register.inclusion_tag("holofood/components/data_type_icons.html", name="data_types")
def data_type_icons(sample: Union[Sample, Animal]) -> dict:
    data_types = {sample_type[0]: False for sample_type in Sample.SAMPLE_TYPE_CHOICES}

    if not sample:
        return data_types
    if type(sample) is Sample:
        data_types[sample.sample_type] = True
    elif type(sample) is Animal and hasattr(sample, "sample_types"):
        for sample_type in sample.sample_types.split(","):
            data_types[sample_type] = True
    return data_types


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


@register.filter(name="significant_digits")
def format_significant_digits_if_number(value, sig_digits: int = 5) -> str:
    if type(value) is not str:
        return value
    try:
        return f"{float(value):.{sig_digits}g}"
    except ValueError:
        return value
