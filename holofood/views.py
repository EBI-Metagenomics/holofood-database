import logging
import operator
from functools import reduce
from typing import List, Type

import requests
from django.core.paginator import Paginator
from django.db.models import Q, Model, CharField, QuerySet, TextField
from django.http import Http404, StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    RedirectView,
)
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import MultipleObjectMixin

from holofood.external_apis.mgnify.api import MgnifyApi
from holofood.filters import (
    SampleFilter,
    MultiFieldSearchFilter,
    GenomeFilter,
    ViralFragmentFilter,
    AnimalFilter,
    GenomeSampleContainmentFilter,
)
from holofood.models import (
    Sample,
    AnalysisSummary,
    GenomeCatalogue,
    ViralCatalogue,
    ViralFragment,
    Genome,
    Animal,
)
from holofood.utils import holofood_config, find_by_path, write_signpost


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


class SignpostedDetailView(DetailView):
    """
    Adds signposting.org headers to a detail view request.
    These direct robots to the related resources of a landing page
    (in the case of HFDP, that means the API endpoint and spec).
    The collection an item is obtained from is also linked to,
    i.e. the relevant list view of the API.
    """

    api_url_name: str
    api_url_args_from_context_path = {"accession": "object.pk"}
    api_list_url_name: str

    DESCRIBED_BY = "describedby"
    COLLECTION = "collection"
    JSON = "application/json"

    def render_to_response(self, context, **response_kwargs):
        described_by_signpost = reverse(
            self.api_url_name,
            kwargs={
                url_param: find_by_path(context, path)
                for url_param, path in self.api_url_args_from_context_path.items()
            },
        )

        headers = response_kwargs.setdefault("headers", {})
        links = headers.get("Link", "")

        if links and not links.endswith(","):
            links += ", "
        links += write_signpost(
            described_by_signpost,
            self.JSON,
            self.DESCRIBED_BY,
            reverse("api:openapi-json"),
        )

        collection_signpost = reverse(self.api_list_url_name)
        links += ", " + write_signpost(
            collection_signpost, self.JSON, self.COLLECTION, reverse("api:openapi-json")
        )

        headers["Link"] = links
        response_kwargs["headers"] = headers
        return super().render_to_response(context, **response_kwargs)


class SampleListView(ListFilterView):
    model = Sample
    context_object_name = "samples"
    paginate_by = 10
    template_name = "holofood/pages/sample_list.html"
    filterset_class = SampleFilter

    def get_context_data(self, **kwargs):
        """
        If the animal accession filter resolves to a single animal,
        set it as "from_animal" so that we can render the list as being
        a single-animal focus.
        """
        context = super().get_context_data(**kwargs)

        filters = self.filterset.data
        animal_filter = filters.get("animal_accession__icontains")
        if animal_filter:
            if Animal.objects.filter(accession__iexact=animal_filter).exists():
                context["from_animal"] = animal_filter

        return context


class SampleDetailView(SignpostedDetailView):
    model = Sample
    context_object_name = "sample"
    template_name = "holofood/pages/sample_detail.html"

    api_url_name = "api:sample_detail"
    api_url_args_from_context_path = {"sample_accession": "sample.pk"}
    api_list_url_name = "api:list_samples"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model: Sample = context["sample"]

        if model.is_metagenomic_sample:
            mgnify = MgnifyApi()

            try:
                context["analyses"] = mgnify.get_metagenomics_analyses_for_sample(
                    model.accession
                )

            except Exception as e:
                logging.error(f"Could not retrieve analyses from MGnify for {model}")
                logging.error(e)
                context["analyses"] = []
                context["analyses_error"] = True

        if model.sample_type in [Sample.METABOLOMIC, Sample.METABOLOMIC_TARGETED]:
            context["assays"] = model.get_metabolights_files()

        if model.is_sequencing_sample:
            context["ena_records"] = model.get_ena_records()

        return context


class AnimalListView(ListFilterView):
    model = Animal
    context_object_name = "animals"
    paginate_by = 10
    template_name = "holofood/pages/animal_list.html"
    filterset_class = AnimalFilter
    ordering = "accession"


class AnimalDetailView(SignpostedDetailView):
    model = Animal
    context_object_name = "animal"
    template_name = "holofood/pages/animal_detail.html"

    api_url_name = "api:animal_detail"
    api_url_args_from_context_path = {"animal_accession": "object.pk"}
    api_list_url_name = "api:list_animals"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("structured_metadata")


class CustomPaginator(Paginator):
    page_param = "page"

    def __init__(self, *args, **kwargs):
        page_param = kwargs.pop("page_param", "page")
        self.page_param = page_param
        super().__init__(*args, **kwargs)


class AnalysisSummaryDetailView(DetailView):
    model = AnalysisSummary
    context_object_name = "analysis_summary"
    template_name = "holofood/pages/analysis_summary_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model: AnalysisSummary = context["analysis_summary"]

        for related_object_type in [
            "samples",
            "genome_catalogues",
            "viral_catalogues",
        ]:
            objects = getattr(model, related_object_type).all()
            objects_paginated = CustomPaginator(
                objects, per_page=10, page_param=f"{related_object_type}_page"
            )
            objects_page = objects_paginated.page(
                kwargs.get(f"{related_object_type}_page", 1)
            )
            context[related_object_type] = objects_page
            context[f"has_{related_object_type}"] = objects.exists()
        print(context)
        return context


class AnalysisSummaryListView(ListFilterView):
    model = AnalysisSummary
    context_object_name = "analysis_summaries"
    template_name = "holofood/pages/analysis_summary_list.html"
    filterset_class = MultiFieldSearchFilter
    ordering = "-updated"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class HomeView(TemplateView):
    template_name = "holofood/pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["samples_count"] = Sample.objects.count()
        context["mags_count"] = Genome.objects.count()
        context["viral_count"] = ViralFragment.objects.count()
        context["analysis_summaries_count"] = AnalysisSummary.objects.filter(
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
    related_ordering = None
    context_related_objects_name = None
    paginate_by = 10

    def get_context_data(self, **kwargs):
        detail_obj = self.get_object()
        assert hasattr(detail_obj, self.related_name)
        related_objects = getattr(detail_obj, self.related_name)
        if hasattr(self, "filterset_class"):
            filterset = self.filterset_class(self.request.GET, queryset=related_objects)
            related_objects = filterset.qs.order_by(self.related_ordering).all()
        else:
            filterset = None
            related_objects = related_objects.order_by(self.related_ordering).all()
        context = super().get_context_data(object_list=related_objects, **kwargs)
        context["filterset"] = filterset
        context_related_name = self.context_related_objects_name or self.related_name
        context[context_related_name] = context["object_list"]
        return context


class GenomeCatalogueView(SignpostedDetailView, DetailViewWithPaginatedRelatedList):
    model = GenomeCatalogue
    context_object_name = "catalogue"
    paginate_by = 10
    template_name = "holofood/pages/genome_catalogue_detail.html"
    filterset_class = GenomeFilter

    related_name = "genomes"
    related_ordering = "accession"

    api_url_name = "api:get_genome_catalogue"
    api_url_args_from_context_path = {"catalogue_id": "object.pk"}
    api_list_url_name = "api:list_genome_catalogues"

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


class GenomeDetailView(SignpostedDetailView, DetailViewWithPaginatedRelatedList):
    model = Genome
    context_object_name = "genome"
    paginate_by = 10
    template_name = "holofood/pages/genome_detail.html"
    filterset_class = GenomeSampleContainmentFilter

    related_name = "samples_containing"
    related_ordering = "-containment"

    api_url_name = "api:get_genome"
    api_url_args_from_context_path = {
        "genome_id": "object.pk",
        "genome_catalogue_id": "object.catalogue_id",
    }
    api_list_url_name = "api:list_genome_catalogues"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalogue"] = get_object_or_404(
            GenomeCatalogue, id=self.kwargs.get("catalogue_pk")
        )
        cazy = self.object.annotations.get("cazy")
        if cazy:
            cazy_categories = {
                "GH": "Glycoside Hydrolase",
                "CB": "Carbohydrate-Binding",
                "PL": "Polysaccharide Lyases",
                "CE": "Carbohydrate Esterases",
                "AA": "Auxiliary Activities",
                "GT": "GlycosylTransferases",
            }
            context["cazy_annotations"] = {
                cazy_categories[cat]: count
                for cat, count in cazy.items()
                if cat in cazy_categories
            }
        else:
            context["cazy_annotations"] = {}
        return context


class ViralCatalogueView(DetailViewWithPaginatedRelatedList):
    model = ViralCatalogue
    context_object_name = "catalogue"
    paginate_by = 10
    template_name = "holofood/pages/viral_catalogue_detail.html"
    filterset_class = ViralFragmentFilter

    related_name = "viral_fragments"
    related_ordering = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["catalogues"] = ViralCatalogue.objects.all()
        context["SHOWALL"] = ViralFragmentFilter.ALL
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
            return reverse("viral_catalogues_empty_state")
        return reverse("viral_catalogue", kwargs={"pk": catalogue.id})


class ViralCataloguesEmptyStateView(TemplateView):
    template_name = "holofood/pages/viral_catalogues_empty_state.html"


class ViralSequenceAnnotationView(BaseDetailView):
    queryset = ViralFragment.objects

    def render_to_response(self, context):
        obj: ViralFragment = context["object"]

        def stream_annotations(gff: str):
            annotations = gff.splitlines()
            for anno in annotations:
                yield anno + "\n"

        response = StreamingHttpResponse(
            stream_annotations(obj.gff), content_type="text/x-gff3"
        )
        response["Content-Disposition"] = f"attachment; filename={obj.id}.gff"
        return response


class GlobalSearchView(TemplateView):
    template_name = "holofood/pages/search.html"

    def multi_search_model(
        self, model: Type[Model], fields: List[str] = None, limit: int = 10
    ) -> QuerySet:
        query = self.request.GET.get("query")
        if not query:
            return model.objects.none()

        fields = fields or list(
            map(
                lambda field: field.name,
                filter(
                    lambda field: isinstance(field, CharField)
                    or isinstance(field, TextField),
                    model._meta.fields,
                ),
            )
        )

        logging.info(f"Will search model {model._meta.label} {fields = } for {query}")

        return model.objects.filter(
            reduce(
                operator.or_,
                (Q(**{f"{field}__icontains": query}) for field in fields),
            )
        )

    def get_docs_results(self) -> List[dict]:
        query = self.request.GET.get("query")
        try:
            logging.info(
                f"Getting docs search JSON from {holofood_config.docs.docs_url}"
            )
            quarto_search_response = requests.get(
                holofood_config.docs.docs_url + "/search.json", timeout=5
            )
            quarto_sections = quarto_search_response.json()
        except Exception as e:
            logging.error("Failed to retrieve docs search items from Quarto")
            logging.error(e)
            return []
        matches = list(
            filter(
                lambda sec: query.lower() in sec.get("text", "").lower(),
                quarto_sections,
            )
        )
        logging.info(f"Found {len(matches)} docs matches for {query}")
        return matches

    @staticmethod
    def get_detail_url_if_accession(query: str):
        query_upper = query.upper()
        if " " in query:
            return
        if (
            query_upper.startswith("SAM")
            and Sample.objects.filter(accession=query_upper).exists()
        ):
            logging.info(f"{query_upper} is a sample accession. Redirecting.")
            return reverse("sample_detail", args=[query_upper])
        if (
            query_upper.startswith("SAM")
            and Animal.objects.filter(accession=query_upper).exists()
        ):
            logging.info(f"{query_upper} is an animal accession. Redirecting.")
            return reverse("animal_detail", args=[query_upper])
        if query_upper.startswith("MGYG"):
            mag = Genome.objects.filter(accession=query_upper).first()
            if mag:
                logging.info(f"{query_upper} is a MAG accession. Redirecting.")
                return (
                    reverse("genome_catalogue", args=[mag.catalogue_id])
                    + f"?accession__icontains={mag.accession}"
                )

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        logging.info(f"Global search for {query}")
        detail_url = self.get_detail_url_if_accession(query)
        if detail_url:
            return redirect(detail_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("query")
        context["samples"] = self.multi_search_model(Sample)
        context["animals"] = self.multi_search_model(Animal)
        context["mag_catalogues"] = self.multi_search_model(GenomeCatalogue)
        context["mags"] = self.multi_search_model(Genome)
        context["viral_catalogues"] = self.multi_search_model(ViralCatalogue)
        context["viral_fragments"] = self.multi_search_model(ViralFragment)
        context["analysis_summaries"] = self.multi_search_model(AnalysisSummary)
        context["docs_sections"] = self.get_docs_results()

        return context
