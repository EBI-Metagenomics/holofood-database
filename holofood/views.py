from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView

from holofood.filters import SampleFilter, MultiFieldSearchFilter
from holofood.models import Sample, SampleAnnotation


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
