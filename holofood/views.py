from django.views.generic import ListView, DetailView

from holofood.filters import SampleFilter
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


class AnnotationDetailView(DetailView):
    model = SampleAnnotation
    context_object_name = "annotation"
    template_name = "holofood/pages/annotation_detail.html"
