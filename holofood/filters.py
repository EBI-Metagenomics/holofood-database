import operator
from functools import reduce

import django_filters
from django.db.models import Q, CharField

from holofood.models import Sample


class MultiFieldSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="multiple_icontains", label="Search")

    class Meta:
        fields = ["search"]

    def multiple_icontains(self, queryset, name, value):
        fields = filter(
            lambda field: isinstance(field, CharField), self.queryset.model._meta.fields
        )
        return queryset.filter(
            reduce(
                operator.or_,
                (Q(**{f"{field.name}__icontains": value}) for field in fields),
            )
        )


class SampleFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=("accession", "project__accession", "title"),
    )

    class Meta:
        model = Sample

        fields = {
            "system": ["exact"],
            "accession": ["icontains"],
            "project__accession": ["icontains"],
            "project__title": ["icontains"],
            "title": ["icontains"],
        }
