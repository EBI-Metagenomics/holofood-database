import operator
from functools import reduce

import django_filters
from django.db.models import Q, CharField, TextField
from django.utils.safestring import mark_safe

from holofood.models import Sample, Genome, ViralFragment, Animal


class MultiFieldSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="multiple_icontains", label="Search")

    class Meta:
        fields = ["search"]

    def multiple_icontains(self, queryset, name, value):
        fields = filter(
            lambda field: isinstance(field, CharField) or isinstance(field, TextField),
            self.queryset.model._meta.fields,
        )
        return queryset.filter(
            reduce(
                operator.or_,
                (Q(**{f"{field.name}__icontains": value}) for field in fields),
            )
        )


class SampleFilter(django_filters.FilterSet):
    animal_accession__icontains = django_filters.CharFilter(
        field_name="animal__accession",
        label="Animal accession contains",
        lookup_expr="icontains",
        help_text=mark_safe(
            f'See <a class="vf-link" href="/animals">the list of animals</a> for details'
        ),
    )

    ordering = django_filters.OrderingFilter(
        fields=("accession", "animal__accession", "title"),
    )

    class Meta:
        model = Sample

        fields = {
            "animal__system": ["exact"],
            "sample_type": ["exact"],
            "accession": ["icontains"],
            "title": ["icontains"],
        }


class AnimalFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=("accession", "samples_count"),
    )

    class Meta:
        model = Animal

        fields = {
            "system": ["exact"],
            "accession": ["icontains"],
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

    cluster_representative_id_contains = django_filters.CharFilter(
        method="cluster_representative_id", label="Cluster representative contains"
    )

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
            "viral_type": ["exact"],
            "host_mag__taxonomy": ["icontains"],
            "host_mag__accession": ["icontains"],
        }

    def cluster_representative_status(self, queryset, name, value):
        if value == self.ALL:
            return queryset
        else:
            return queryset.filter(cluster_representative__isnull=True)

    def cluster_representative_id(self, queryset, name, value):
        matches_representative = Q(id__icontains=value)
        matches_member = Q(cluster_representative__id__icontains=value)
        return queryset.filter(matches_member | matches_representative)

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            if not data.get("cluster_visibility"):
                data["cluster_visibility"] = self.REPS

        super().__init__(data, *args, **kwargs)
