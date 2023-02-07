import operator
from enum import Enum
from functools import reduce
from typing import Optional, List

from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.urls import reverse
from ninja import ModelSchema, NinjaAPI, Field
from ninja.pagination import RouterPaginated
from pydantic import AnyHttpUrl

from holofood.models import (
    Sample,
    Project,
    SampleStructuredDatum,
    SampleMetadataMarker,
    AnalysisSummary,
    GenomeCatalogue,
    Genome,
    ViralCatalogue,
    ViralFragment,
)
from holofood.utils import holofood_config

api = NinjaAPI(
    title="HoloFood Data Portal API",
    description="The API to browse [HoloFood](https://www.holofood.eu) samples and metadata, "
    "and navigate to datasets stored in public archives. \n\n #### Useful links: \n"
    "- [Documentation](https://ebi-metagenomics.github.io/holofood-database/)\n"
    "- [HoloFood Data Portal home](/)\n"
    "- [HoloFood Project Website](https://www.holofood.eu)\n"
    "- [Helpdesk](https://www.ebi.ac.uk/contact)\n"
    "- [TSV Export endpoints](/export/docs)",
    urls_namespace="api",
    default_router=RouterPaginated(),
    csrf=True,
)


class RelatedProjectSchema(ModelSchema):
    @staticmethod
    def resolve_canonical_url(obj: Project):
        return f"{holofood_config.ena.browser_url}/{obj.accession}"

    canonical_url: str

    class Config:
        model = Project
        model_fields = ["accession", "title"]


class SampleMetadataMarkerSchema(ModelSchema):
    canonical_url: str = Field(None, alias="iri")

    class Config:
        model = SampleMetadataMarker
        model_fields = ["name", "type"]


class SampleCountedMetadataMarkerSchema(SampleMetadataMarkerSchema):
    samples_count: int


class SampleStructuredDatumSchema(ModelSchema):
    marker: SampleMetadataMarkerSchema

    class Config:
        model = SampleStructuredDatum
        model_fields = ["marker", "measurement", "units"]


class RelatedAnalysisSummarySchema(ModelSchema):
    @staticmethod
    def resolve_canonical_url(obj: AnalysisSummary):
        return reverse("analysis_summary_detail", kwargs={"slug": obj.slug})

    canonical_url: str

    class Config:
        model = AnalysisSummary
        model_fields = ["title"]


class SampleSlimSchema(ModelSchema):
    project: RelatedProjectSchema

    @staticmethod
    def resolve_canonical_url(obj: Sample):
        return f"{holofood_config.ena.browser_url}/{obj.accession}"

    canonical_url: str

    @staticmethod
    def resolve_metagenomics_url(obj: Sample):
        return (
            f"{holofood_config.mgnify.api_root}/samples/{obj.accession}"
            if obj.has_metagenomics
            else None
        )

    metagenomics_url: Optional[str]

    @staticmethod
    def resolve_metabolomics_url(obj: Sample):
        return (
            f"{holofood_config.metabolights.api_root}/studies/{obj.metabolights_project}"
            if obj.has_metabolomics
            else None
        )

    metabolomics_url: Optional[str]

    class Config:
        model = Sample
        model_fields = [
            "accession",
            "title",
            "project",
            "system",
            "has_metagenomics",
            "has_metabolomics",
        ]


class SampleSchema(SampleSlimSchema):
    structured_metadata: List[SampleStructuredDatumSchema]
    analysis_summaries: List[RelatedAnalysisSummarySchema]

    @staticmethod
    def resolve_project_analysis_summaries(obj: Sample):
        return obj.project.analysis_summaries.all()

    project_analysis_summaries: List[RelatedAnalysisSummarySchema]


class AnalysisSummarySchema(RelatedAnalysisSummarySchema):
    samples: List[SampleSlimSchema]
    projects: List[RelatedProjectSchema]

    class Config:
        model = AnalysisSummary
        model_fields = ["title"]


class GenomeCatalogueSchema(ModelSchema):
    class Config:
        model = GenomeCatalogue
        model_fields = ["id", "title", "biome", "related_mag_catalogue_id", "system"]


class GenomeSchema(ModelSchema):
    @staticmethod
    def resolve_representative_url(obj: Genome):
        return f"{holofood_config.mgnify.api_root}/genomes/{obj.cluster_representative}"

    representative_url: Optional[str]

    class Config:
        model = Genome
        model_fields = ["accession", "cluster_representative", "taxonomy", "metadata"]


class ViralCatalogueSchema(ModelSchema):
    related_genome_catalogue: GenomeCatalogueSchema

    @staticmethod
    def resolve_related_genome_catalogue_url(obj: ViralCatalogue):
        return reverse(
            "api:get_genome_catalogue",
            kwargs={"catalogue_id": obj.related_genome_catalogue_id},
        )

    related_genome_catalogue_url: str

    class Config:
        model = ViralCatalogue
        model_fields = ["id", "title", "biome", "system"]


class ViralFragmentSchema(ModelSchema):
    cluster_representative: Optional["ViralFragmentSchema"]
    host_mag: Optional[GenomeSchema]

    @staticmethod
    def resolve_contig_url(obj: ViralFragment):
        return f"{holofood_config.mgnify.api_root}/analyses/{obj.mgnify_analysis_accession}/contigs/{obj.contig_id}"

    contig_url: AnyHttpUrl

    @staticmethod
    def resolve_mgnify_analysis_url(obj: ViralFragment):
        return f"{holofood_config.mgnify.api_root}/analyses/{obj.mgnify_analysis_accession}"

    mgnify_analysis_url: AnyHttpUrl

    @staticmethod
    def resolve_gff_url(obj: ViralFragment):
        return reverse("viral_fragment_gff", kwargs={"pk": obj.id})

    gff_url: str

    class Config:
        model = ViralFragment
        model_fields = [
            "id",
            "contig_id",
            "mgnify_analysis_accession",
            "start_within_contig",
            "end_within_contig",
            "metadata",
            "host_mag",
            "viral_type",
        ]


SAMPLES = "Samples"
ANALYSES = "Analysis Summaries"
GENOMES = "Genomes"
VIRUSES = "Viruses"


class System(Enum):
    salmon: str = Sample.SALMON
    chicken: str = Sample.CHICKEN


@api.get(
    "/samples/{sample_accession}",
    response=SampleSchema,
    summary="Fetch a single Sample from the HoloFood database.",
    description="Retrieve a single Sample by its ENA accession, including all structured metadata available. ",
    url_name="sample_detail",
    tags=[SAMPLES],
)
def get_sample(request, sample_accession: str):
    sample = get_object_or_404(Sample, accession=sample_accession)
    return sample


@api.get(
    "/samples",
    response=List[SampleSlimSchema],
    summary="Fetch a list of Samples.",
    description="Long lists will be paginated, so use the `page=` query parameter to get more pages. "
    "Several filters are available, which mostly perform case-insensitive containment lookups. "
    "Sample metadata are *not* returned for each item. "
    "Use the `/samples/{sample_accession}` endpoint to retrieve those. "
    "Sample metadata *can* be filtered for with `require_metadata_marker=`: this finds samples where "
    "the named metadata marker is present and none of `['0', 'false', 'unknown', 'n/a', 'null]`. "
    "Use `/sample_metadata_markers` to find the exact marker name of interest.",
    tags=[SAMPLES],
)
def list_samples(
    request,
    system: System = None,
    accession: str = None,
    project_accession: str = None,
    project_title: str = None,
    title: str = None,
    require_metagenomics: bool = False,
    require_metabolomics: bool = False,
    require_metadata_marker: str = None,
):
    q_objects = []
    if system:
        q_objects.append(Q(system__icontains=system.value))
    if accession:
        q_objects.append(Q(accession__icontains=accession))
    if project_accession:
        q_objects.append(Q(project__accession__icontains=project_accession))
    if project_title:
        q_objects.append(Q(project__title__icontains=project_title))
    if title:
        q_objects.append(Q(title__icontains=title))
    if require_metagenomics:
        q_objects.append(Q(has_metagenomics=True))
    if require_metabolomics:
        q_objects.append(Q(has_metabolomics=True))
    if require_metadata_marker:
        sample_ids_with_metadata = (
            SampleStructuredDatum.objects.filter(
                marker__name__iexact=require_metadata_marker
            )
            .annotate(measurement_lower=Lower("measurement"))
            .exclude(measurement_lower__in=("0", "false", "unknown", "n/a", "null"))
            .values_list("sample_id", flat=True)
        )
        q_objects.append(Q(accession__in=sample_ids_with_metadata))
    if not q_objects:
        return Sample.objects.all()
    return Sample.objects.filter(reduce(operator.and_, q_objects))


@api.get(
    "/sample_metadata_markers",
    response=List[SampleCountedMetadataMarkerSchema],
    summary="Fetch a list of structured metadata markers (i.e. keys).",
    description="Each marker is present in the metadata of at least one sample. "
    "Not every sample will have every metadata marker. "
    "Long lists will be paginated, so use the `page=` query parameter to get more pages. "
    "Use `name=` to search for a marker by name (case insensitive partial matches). "
    "Use `min_samples=` to search for markers present on at least that many samples.",
    tags=[SAMPLES],
)
def list_sample_metadata_markers(
    request,
    name: str = None,
    min_samples: int = None,
):
    q_objects = []
    if name:
        q_objects.append(Q(name__icontains=name))
    if min_samples:
        q_objects.append(Q(samples_count__gte=min_samples))

    annotated_markers = SampleMetadataMarker.objects.annotate(
        samples_count=models.Count("samplestructureddatum")
    )
    if not q_objects:
        return annotated_markers.all()
    return annotated_markers.filter(reduce(operator.and_, q_objects))


@api.get(
    "/analysis-summaries",
    response=List[AnalysisSummarySchema],
    summary="Fetch a list of Analysis Summary documents.",
    description="Analysis Summary documents are produced by HoloFood partners and collaborators. "
    "Each summary is tagged as involving 1 or more Samples, Projects, or Catalogues. "
    "Typically these are aggregative or comparative analyses of the Samples. "
    "These are text and graphic documents. "
    "They are not intended for programmatic consumption, so a website URL is returned for each. ",
    tags=[ANALYSES],
)
def list_analysis_summaries(
    request,
):
    return AnalysisSummary.objects.filter(is_published=True)


@api.get(
    "/genome-catalogues",
    response=List[GenomeCatalogueSchema],
    summary="Fetch a list of Genome (MAG) Catalogues",
    description="Genome Catalogues are lists of Metagenomic Assembled Genomes (MAGs)"
    "MAGs originating from HoloFood samples are organised into biome-specific catalogues.",
    tags=[GENOMES],
)
def list_genome_catalogues(request):
    return GenomeCatalogue.objects.all()


@api.get(
    "/genome-catalogues/{catalogue_id}",
    response=GenomeCatalogueSchema,
    summary="Fetch a single Genome Catalogue",
    description="A Genome Catalogue is a list of Metagenomic Assembled Genomes (MAGs)."
    "MAGs originating from HoloFood samples are organised into biome-specific catalogues."
    "To list the genomes for a catalogue, use `/genome-catalogues/{catalogue_id}/genomes`.",
    url_name="get_genome_catalogue",
    tags=[GENOMES],
)
def get_genome_catalogue(request, catalogue_id: str):
    catalogue = get_object_or_404(GenomeCatalogue, id=catalogue_id)
    return catalogue


@api.get(
    "/genome-catalogues/{catalogue_id}/genomes",
    response=List[GenomeSchema],
    summary="Fetch the list of Genomes within a Catalogue",
    description="Genome Catalogues are lists of Metagenomic Assembled Genomes (MAGs)."
    "MAGs listed originate from HoloFood samples."
    "Each MAG has also been clustered with MAGs from other projects."
    "Each HoloFood MAG references the best representative of these clusters, in MGnify.",
    tags=[GENOMES],
)
def list_genome_catalogue_genomes(request, catalogue_id: str):
    catalogue = get_object_or_404(GenomeCatalogue, id=catalogue_id)
    return catalogue.genomes.all()


@api.get(
    "/viral-catalogues",
    response=List[ViralCatalogueSchema],
    summary="Fetch a list of Viral (contig fragment) Catalogues",
    description="Viral Catalogues are lists of Viral Sequences,"
    "detected in the assembly contigs of HoloFood samples from a specific biome.",
    tags=[VIRUSES],
)
def list_viral_catalogues(request):
    return ViralCatalogue.objects.all()


@api.get(
    "/viral-catalogues/{catalogue_id}",
    response=ViralCatalogueSchema,
    summary="Fetch a single Viral Catalogue",
    description="A Viral Catalogue is a list of Viral Sequences,"
    "detected in the assembly contigs of HoloFood samples from a specific biome."
    "To list the viral sequences (“fragments”) for a catalogue, use `/viral-catalogues/{catalogue_id}/fragments`.",
    tags=[VIRUSES],
)
def get_viral_catalogue(request, catalogue_id: str):
    catalogue = get_object_or_404(ViralCatalogue, id=catalogue_id)
    return catalogue


@api.get(
    "/viral-catalogues/{catalogue_id}/fragments",
    response=List[ViralFragmentSchema],
    summary="Fetch the list of viral fragments (sequences) from a Catalogue",
    description="Viral fragments are sequences predicted to be viral, "
    "found in the assembly contigs of HoloFood samples."
    "The Catalogue’s viral fragments are all from the same biome."
    "Viral sequences are clustered by sequence identity, at a species-level."
    "Both cluster representatives and cluster members are included."
    "Where a viral sequence is found in a related MAG (metagenome assembly genome,"
    " e.g. a bacterial species), this MAG is considered a “host MAG”.",
    tags=[VIRUSES],
)
def list_viral_catalogue_fragments(request, catalogue_id: str):
    catalogue = get_object_or_404(ViralCatalogue, id=catalogue_id)
    return catalogue.viral_fragments.all()
