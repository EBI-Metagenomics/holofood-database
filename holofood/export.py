import csv
from io import StringIO
from typing import MutableMapping, List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer

from holofood.api import (
    SampleSlimSchema,
    SampleStructuredDatumSchema,
    GenomeSchema,
    ViralFragmentSchema,
    AnimalSlimSchema,
    AnimalStructuredDatumSchema,
    GenomeSampleContainmentSchema,
)
from holofood.models import Sample, GenomeCatalogue, ViralCatalogue, Animal, Genome


class CSVRenderer(BaseRenderer):
    media_type = "text/tab-separated-values"

    @classmethod
    def _flatten_data_generator(cls, dict_field: MutableMapping, parent_path: str = ""):
        for field, fielddata in dict_field.items():
            path = f"{parent_path}__{field}" if parent_path else field
            if isinstance(fielddata, MutableMapping):
                yield from cls._flatten_data(fielddata, path).items()
            else:
                yield path, fielddata

    @classmethod
    def _flatten_data(cls, dict_field: MutableMapping, parent_path: str = ""):
        return dict(cls._flatten_data_generator(dict_field, parent_path))

    def render(self, request, data, *, response_status):
        stream = StringIO()
        csv_data = csv.writer(stream, delimiter="\t")

        for idx, obj in enumerate(data):
            if idx == 0:
                headers = self._flatten_data(obj).keys()
                csv_data.writerow(headers)
            csv_data.writerow(self._flatten_data(obj).values())
        return stream.getvalue()


export_api = NinjaAPI(
    title="HoloFood Data Portal Export API",
    description="Download TSV exports of the HoloFood Data Portal data.",
    urls_namespace="export",
    csrf=True,
    renderer=CSVRenderer(),
)


@export_api.get(
    "/samples",
    response=List[SampleSlimSchema],
    summary="Fetch a list of Samples as a TSV",
    url_name="samples_list",
)
def list_samples(
    request,
):
    return Sample.objects.all()


@export_api.get(
    "/samples/{sample_accession}/metadata",
    response=List[SampleStructuredDatumSchema],
    summary="Fetch a list of a Sample's metadata as a TSV.",
    description="Retrieve a table of metadata for a single Sample by its ENA accession.",
    url_name="sample_metadata_list",
)
def get_sample_metadata(request, sample_accession: str):
    sample = get_object_or_404(Sample, accession=sample_accession)
    return sample.structured_metadata.all()


@export_api.get(
    "/animals",
    response=List[AnimalSlimSchema],
    summary="Fetch a list of Animals (host-level BioSamples) as a TSV",
    url_name="animals_list",
)
def list_animals(
    request,
):
    return Animal.objects.all()


@export_api.get(
    "/animals/{animal_accession}/metadata",
    response=List[AnimalStructuredDatumSchema],
    summary="Fetch a list of an Animal's metadata as a TSV.",
    description="Retrieve a table of metadata for a single Animal by its BioSamples accession.",
    url_name="animal_metadata_list",
)
def get_animal_metadata(request, animal_accession: str):
    animal = get_object_or_404(Animal, accession=animal_accession)
    return animal.structured_metadata.all()


@export_api.get(
    "/genome-catalogues/{catalogue_id}/genomes",
    response=List[GenomeSchema],
    summary="Fetch the list of Genomes from a Catalogue as a TSV",
    description="Download a TSV export of the Genome Catalogue MAGs",
    url_name="genomes_list",
)
def list_genome_catalogue_genomes(request, catalogue_id: str):
    catalogue = get_object_or_404(GenomeCatalogue, id=catalogue_id)
    return catalogue.genomes.all()


@export_api.get(
    "/genome-catalogues/{genome_catalogue_id}/genomes/{genome_id}/samples_containing",
    response=List[GenomeSampleContainmentSchema],
    summary="Fetch the list of Samples contained by a Genome, as a TSV",
    description="A Genomes is a Metagenomic Assembled Genome (MAG)."
    "Each MAG originates from HoloFood samples."
    "Each MAG has also been clustered with MAGs from other projects."
    "Each HoloFood MAG references the best representative of these clusters, in MGnify."
    "Each species representative MAG has also been searched in all of the project samples, "
    "to find samples which contain the kmers of genome.",
    url_name="get_samples_containing_genome",
)
def get_genome(request, genome_catalogue_id: str, genome_id: str):
    genome = get_object_or_404(Genome, accession=genome_id)
    return genome.samples_containing


@export_api.get(
    "/viral-catalogues/{catalogue_id}/fragments",
    response=List[ViralFragmentSchema],
    summary="Fetch the list of Viral Fragments (sequences) from a Catalogue as a TSV",
    description="Download a TSV export of the Viral Catalogue fragments",
    url_name="viral_fragments_list",
)
def list_viral_catalogue_fragments(request, catalogue_id: str):
    catalogue = get_object_or_404(ViralCatalogue, id=catalogue_id)
    return catalogue.viral_fragments.all()
