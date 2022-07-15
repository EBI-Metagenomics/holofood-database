import operator
from functools import reduce

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView, RedirectView
from django.views.generic.list import MultipleObjectMixin

from holofood.external_apis.mgnify.api import get_metagenomics_analyses_for_run
from holofood.filters import (
    SampleFilter,
    MultiFieldSearchFilter,
    GenomeFilter,
    ViralFragmentFilter,
)
from holofood.models import (
    Sample,
    SampleAnnotation,
    GenomeCatalogue,
    ViralCatalogue,
    ViralFragment,
)


class ListFilterView(ListView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class SampleListView(ListFilterView):
    model = Sample
    context_object_name = "samples"
    paginate_by = 10
    template_name = "holofood/pages/sample_list.html"
    filterset_class = SampleFilter


class SampleDetailView(DetailView):
    model = Sample
    context_object_name = "sample"
    template_name = "holofood/pages/sample_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model: Sample = context["sample"]

        context["analyses"] = reduce(
            operator.concat, map(get_metagenomics_analyses_for_run, model.runs), []
        )

        return context


class CustomPaginator(Paginator):
    page_param = "page"

    def __init__(self, *args, **kwargs):
        page_param = kwargs.pop("page_param", "page")
        self.page_param = page_param
        super().__init__(*args, **kwargs)


class AnnotationDetailView(DetailView):
    model = SampleAnnotation
    context_object_name = "annotation"
    template_name = "holofood/pages/annotation_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model: SampleAnnotation = context["annotation"]

        samples = model.samples.all()
        samples_paginated = CustomPaginator(
            samples, per_page=10, page_param="samples_page"
        )
        samples_page = samples_paginated.page(kwargs.get("samples_page", 1))
        context["samples"] = samples_page

        projects = model.projects.all()
        projects_paginated = CustomPaginator(
            projects, per_page=10, page_param="projects_page"
        )
        projects_page = projects_paginated.page(kwargs.get("projects_page", 1))
        context["projects"] = projects_page

        return context


class AnnotationListView(ListFilterView):
    model = SampleAnnotation
    context_object_name = "annotations"
    template_name = "holofood/pages/annotation_list.html"
    filterset_class = MultiFieldSearchFilter
    ordering = "-updated"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class HomeView(TemplateView):
    template_name = "holofood/pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["samples_count"] = Sample.objects.count()
        context["annotations_count"] = SampleAnnotation.objects.filter(
            is_published=True
        ).count()
        return context


class DetailViewWithPaginatedRelatedList(DetailView, MultipleObjectMixin):
    """
    A detail (single object) view that also supports pagination of a list of related objects
    E.g., use this for a catalogue detail view which renders a paginated list of entries.
    Set `related_name = 'entries'` if Entry has a foreign key to Catalogue with related_name='entries'.
    Set `context_related_objects_name = 'cat_entries'` to use {% for entry in cat_entries %} in the template.
    """

    related_name = None
    context_related_objects_name = None
    paginate_by = 10

    def get_context_data(self, **kwargs):
        detail_obj = self.get_object()
        assert hasattr(detail_obj, self.related_name)
        related_objects = getattr(detail_obj, self.related_name)
        if hasattr(self, "filterset_class"):
            filterset = self.filterset_class(self.request.GET, queryset=related_objects)
            related_objects = filterset.qs.all()
        else:
            filterset = None
            related_objects = related_objects.all()
        context = super().get_context_data(object_list=related_objects, **kwargs)
        context["filterset"] = filterset
        context_related_name = self.context_related_objects_name or self.related_name
        context[context_related_name] = context["object_list"]
        return context


class GenomeCatalogueView(DetailViewWithPaginatedRelatedList):
    model = GenomeCatalogue
    context_object_name = "catalogue"
    paginate_by = 10
    template_name = "holofood/pages/genome_catalogue_detail.html"
    filterset_class = GenomeFilter

    related_name = "genomes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalogues"] = GenomeCatalogue.objects.all()
        return context


class GenomeCataloguesView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        catalogue = GenomeCatalogue.objects.first()
        if not catalogue:
            raise Http404
        return reverse("genome_catalogue", kwargs={"pk": catalogue.id})


class ViralCatalogueView(DetailViewWithPaginatedRelatedList):
    model = ViralCatalogue
    context_object_name = "catalogue"
    paginate_by = 10
    template_name = "holofood/pages/viral_catalogue_detail.html"
    filterset_class = ViralFragmentFilter

    related_name = "viral_fragments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalogues"] = ViralCatalogue.objects.all()
        return context


class ViralCatalogueFragmentView(ViralCatalogueView):
    def get_context_data(self, **kwargs):
        context = super(ViralCatalogueFragmentView, self).get_context_data(**kwargs)
        fragment = get_object_or_404(
            ViralFragment, id=self.kwargs.get("viral_fragment_pk")
        )
        context["selected_viral_fragment"] = fragment
        return context


class ViralCataloguesView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        catalogue = ViralCatalogue.objects.first()
        if not catalogue:
            raise Http404
        return reverse("viral_catalogue", kwargs={"pk": catalogue.id})
