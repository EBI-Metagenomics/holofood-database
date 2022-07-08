import operator
from enum import Enum
from functools import reduce
from typing import Optional

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from ninja import ModelSchema, NinjaAPI, Field
from ninja.pagination import RouterPaginated

from holofood.models import (
    Sample,
    Project,
    SampleStructuredDatum,
    SampleMetadataMarker,
    SampleAnnotation,
    GenomeCatalogue,
    Genome,
)
from holofood.utils import holofood_config

api = NinjaAPI(
    title="HoloFood Data Portal API",
    description="The API to browse [HoloFood](https://www.holofood.eu) samples and metadata, "
    "and navigate to datasets stored in public archives. \n\n #### Useful links: \n"
    "- [Documentation](todo)\n"
    "- [HoloFood Data Portal home](/)\n"
    "- [HoloFood Project Website](https://www.holofood.eu)\n"
    "- [Helpdesk](https://www.ebi.ac.uk/contact)\n",
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


class SampleStructuredDatumSchema(ModelSchema):
    marker: SampleMetadataMarkerSchema

    class Config:
        model = SampleStructuredDatum
        model_fields = ["marker", "measurement", "units"]


class RelatedAnnotationSchema(ModelSchema):
    @staticmethod
    def resolve_canonical_url(obj: SampleAnnotation):
        return reverse("annotation_detail", kwargs={"slug": obj.slug})

    canonical_url: str

    class Config:
        model = SampleAnnotation
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

    class Config:
        model = Sample
        model_fields = ["accession", "title", "project", "system", "has_metagenomics"]


class SampleSchema(SampleSlimSchema):
    structured_metadata: list[SampleStructuredDatumSchema]
    annotations: list[RelatedAnnotationSchema]


class AnnotationSchema(ModelSchema):
    samples: list[SampleSlimSchema]
    projects: list[RelatedProjectSchema]

    class Config:
        model = SampleAnnotation
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


@api.get(
    "/samples/{sample_accession}",
    response=SampleSchema,
    summary="Fetch a single Sample from the HoloFood database.",
    description="Retrieve a single Sample by its ENA accession, including all structured metadata available. ",
    url_name="sample_detail",
)
def get_sample(request, sample_accession: str):
    sample = get_object_or_404(Sample, accession=sample_accession)
    return sample


class System(Enum):
    salmon: str = Sample.SALMON
    chicken: str = Sample.CHICKEN


@api.get(
    "/samples",
    response=list[SampleSlimSchema],
    summary="Fetch a list of Samples.",
    description="Long lists will be paginated, so use the `page=` query parameter to get more pages. "
    "Several filters are available, which mostly perform case-insensitive containment lookups. "
    "Sample metadata are *not* returned for each item. "
    "Use the `/samples/{sample_accession}` endpoint to retrieve those.",
)
def list_samples(
    request,
    system: System = None,
    accession: str = None,
    project_accession: str = None,
    project_title: str = None,
    title: str = None,
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
    if not q_objects:
        return Sample.objects.all()
    return Sample.objects.filter(reduce(operator.and_, q_objects))


@api.get(
    "/annotations",
    response=list[AnnotationSchema],
    summary="Fetch a list of Annotation documents.",
    description="Annotation documents are summaries of analyses conduced by HoloFood partners and collaborators. "
    "Each annotation is tagged as involving 1 or more Samples or Projects. "
    "Typically these are aggregative or comparative analyses of the Samples. "
    "These are text and graphic documents. "
    "They are not intended for programmatic consumption, so a website URL is returned for each. ",
)
def list_annotations(
    request,
):
    return SampleAnnotation.objects.filter(is_published=True)


@api.get(
    "/genome-catalogues",
    response=list[GenomeCatalogueSchema],
    summary="Fetch a list of Genome (MAG) Catalogues",
)
def list_genome_catalogues(request):
    return GenomeCatalogue.objects.all()


@api.get(
    "/genome-catalogues/{catalogue_id}",
    response=GenomeCatalogueSchema,
    summary="Fetch a single Genome Catalogue",
    description="Genome Catalogues are lists of Metagenomic Assembled Genomes (MAGs)."
    "MAGs originating from HoloFood samples are organised into catalogues."
    "To list the genomes for a catalogue, use `/genome-catalogues/{catalogue_id}/genomes`.",
)
def get_genome_catalogue(request, catalogue_id: str):
    catalogue = get_object_or_404(GenomeCatalogue, id=catalogue_id)
    return catalogue


@api.get(
    "/genome-catalogues/{catalogue_id}/genomes",
    response=list[GenomeSchema],
    summary="Fetch the list of Genomes within a Catalogue",
    description="Genome Catalogues are lists of Metagenomic Assembled Genomes (MAGs)."
    "MAGs listed originate from HoloFood samples."
    "Each MAG has also been clustered with MAGs from other projects."
    "Each HoloFood MAG references the best representative of these clusters, in MGnify.",
)
def list_genome_catalogue_genomes(request, catalogue_id: str):
    catalogue = get_object_or_404(GenomeCatalogue, id=catalogue_id)
    return catalogue.genomes.all()
