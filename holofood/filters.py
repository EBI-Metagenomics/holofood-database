import operator
from functools import reduce

import django_filters
from django.db.models import Q, CharField

from holofood.models import Sample, Genome, ViralFragment


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


class GenomeFilter(django_filters.FilterSet):
    class Meta:
        model = Genome

        fields = {
            "accession": ["icontains"],
            "cluster_representative": ["icontains"],
            "taxonomy": ["icontains"],
        }


class ViralFragmentFilter(django_filters.FilterSet):
    ALL = "Include species-cluster members"
    REPS = "Species-cluster representatives only"
    cluster_visibility = django_filters.ChoiceFilter(
        choices=[(ALL, ALL), (REPS, REPS)],
        method="cluster_representative_status",
        label="Cluster visibility",
        help_text="Species-level cluster representatives always shown.",
    )

    class Meta:
        model = ViralFragment

        fields = {
            "id": ["icontains"],
            "contig_id": ["icontains"],
            "cluster_representative__id": ["icontains"],
            "viral_type": ["exact"],
            "host_mag__taxonomy": ["icontains"],
            "host_mag__accession": ["icontains"],
        }

    def cluster_representative_status(self, queryset, name, value):
        if value == self.ALL:
            return queryset
        else:
            return queryset.filter(cluster_representative__isnull=True)

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            if not data.get("cluster_visibility"):
                data["cluster_visibility"] = self.REPS

        super().__init__(data, *args, **kwargs)
