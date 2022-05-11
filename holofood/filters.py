import django_filters

from holofood.models import Sample


class SampleFilter(django_filters.FilterSet):
    class Meta:
        model = Sample
        fields = {
            "system": ["exact"],
            "accession": ["icontains"],
            "project__accession": ["icontains"],
            "project__title": ["icontains"],
            "title": ["icontains"],
        }
