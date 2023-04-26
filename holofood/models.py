import logging
from typing import List

from django.db import models
from django.db.models import Prefetch, Count, Subquery, OuterRef, F
from django.urls import reverse
from django.utils.text import slugify
from martor.models import MartorField

from holofood.external_apis.biosamples.api import (
    get_sample_structured_data,
    get_biosample,
)
from holofood.external_apis.ena.browser_api import get_checklist_metadata
from holofood.external_apis.metabolights.api import get_metabolights_assays

from holofood.external_apis.mgnify.api import MgnifyApi
from holofood.utils import holofood_config, DistinctFunc

_mgnify = MgnifyApi()


class AnimalManager(models.Manager):
    def get_queryset(self):
        prefetchable_markers = (
            holofood_config.tables.animals_list.default_metadata_marker_columns
        )
        primary_markers = AnimalStructuredDatum.objects.filter(
            marker__name__in=prefetchable_markers
        )
        samples = Sample.objects.filter(animal=OuterRef("pk")).order_by("sample_type")
        return (
            super()
            .get_queryset()
            .annotate(samples_count=Count("samples"))
            .annotate(
                sample_types=Subquery(
                    samples.values_list("sample_type", flat=True)
                    .annotate(
                        all_types=DistinctFunc(
                            F("sample_type"), function="GROUP_CONCAT"
                        )
                    )
                    .values("all_types")
                )
            )
            .prefetch_related(
                Prefetch(
                    "structured_metadata",
                    queryset=primary_markers,
                    to_attr="primary_metadata",
                )
            )
        )


class Animal(models.Model):
    """
    A host-level BioSample representing an individual bird or fish,
    from which other samples are derived.
    """

    objects = AnimalManager()
    CHICKEN = "chicken"
    SALMON = "salmon"
    SYSTEM_CHOICES = [(CHICKEN, CHICKEN), (SALMON, SALMON)]

    accession = models.CharField(primary_key=True, max_length=15)
    system = models.CharField(choices=SYSTEM_CHOICES, max_length=10, null=True)

    def refresh_structureddata(self, structured_metadata: dict = None):
        """
        Set the metadata on Animal, either using a dict of structured metadata from BioSamples,
        or optionally fetching that from the BioSamples API.
        :param structured_metadata: Optional dict of metadata sections, e.g. if known from sample import.
        :return:
        """
        if not structured_metadata:
            metadata = get_sample_structured_data(self.accession)
        else:
            metadata = structured_metadata

        for metadata_type, metadata_content in metadata.items():
            if not metadata_content:
                logging.debug(
                    f"{metadata_type=} from {self.accession} was null – skipping"
                )
                continue
            for metadatum in metadata_content:
                marker, created = SampleMetadataMarker.objects.update_or_create(
                    name=metadatum["marker"]["value"],
                    type=metadata_type,
                    defaults={"iri": metadatum["marker"]["iri"]},
                )
                if created:
                    logging.info(f"Created new SampleMetadataMarker {marker}")
                self.structured_metadata.update_or_create(
                    marker=marker,
                    defaults={
                        "source": SampleStructuredDatum.BIOSAMPLES,
                        "measurement": metadatum["measurement"]["value"],
                        "partner_name": metadatum.get("partner", {}).get("value"),
                        "partner_iri": metadatum.get("partner", {}).get("iri"),
                        "units": metadatum.get("measurement_units", {}).get("value"),
                    },
                )


class SampleManager(models.Manager):
    def get_queryset(self):
        prefetchable_markers = (
            holofood_config.tables.animals_list.default_metadata_marker_columns
        )
        primary_markers = AnimalStructuredDatum.objects.filter(
            marker__name__in=prefetchable_markers
        )
        return (
            super()
            .get_queryset()
            .select_related("animal")
            .prefetch_related(
                Prefetch(
                    "animal__structured_metadata",
                    queryset=primary_markers,
                    to_attr="primary_metadata",
                )
            )
        )


class Sample(models.Model):
    """
    An extraction-level BioSample, derived from an Animal.
    """

    METAGENOMIC_ASSEMBLY = "metagenomic_assembly"
    METAGENOMIC_AMPLICON = "metagenomic_amplicon"
    METABOLOMIC = "metabolomic"
    METABOLOMIC_TARGETED = "metabolomic_targeted"
    HISTOLOGICAL = "histological"
    HOST_GENOMIC = "host_genomic"
    TRANSCRIPTOMIC = "transcriptomic"
    META_TRANSCRIPTOMIC = "metatranscriptomic"
    IODINE = "iodine"
    FATTY_ACIDS = "fatty_acids"
    HEAVY_METALS = "heavy_metals"
    INFLAMMATORY_MARKERS = "inflammatory_markers"

    SAMPLE_TYPE_CHOICES = [
        (METAGENOMIC_ASSEMBLY, METAGENOMIC_ASSEMBLY),
        (METAGENOMIC_AMPLICON, METAGENOMIC_AMPLICON),
        (METABOLOMIC, METABOLOMIC),
        (METABOLOMIC_TARGETED, METABOLOMIC_TARGETED),
        (HISTOLOGICAL, HISTOLOGICAL),
        (HOST_GENOMIC, HOST_GENOMIC),
        (TRANSCRIPTOMIC, TRANSCRIPTOMIC),
        (META_TRANSCRIPTOMIC, META_TRANSCRIPTOMIC),
        (IODINE, IODINE),
        (FATTY_ACIDS, FATTY_ACIDS),
        (HEAVY_METALS, HEAVY_METALS),
        (INFLAMMATORY_MARKERS, INFLAMMATORY_MARKERS),
    ]

    objects = SampleManager()

    accession = models.CharField(primary_key=True, max_length=15)

    title = models.CharField(max_length=200)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="samples")

    sample_type = models.CharField(
        max_length=20, choices=SAMPLE_TYPE_CHOICES, null=True, blank=True
    )

    metabolights_study = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"Sample {self.accession} - {self.title}"

    class Meta:
        ordering = ("accession",)

    def refresh_structureddata(
        self, structured_metadata: dict = None, checklist: list = None
    ):
        """
        Set the metadata on Sample, either using a dict of structured metadata from BioSamples,
        or optionally fetching that from the BioSamples API.
        :param checklist: Optional list of checklist data like ENA API returns, e.g. if known from sample import.
        :param structured_metadata: Optional dict of metadata sections, e.g. if known from sample import.
        :return:
        """
        if not structured_metadata:
            metadata = get_sample_structured_data(self.accession)
        else:
            metadata = structured_metadata

        for metadata_type, metadata_content in metadata.items():
            if not metadata_content:
                logging.debug(
                    f"{metadata_type=} from {self.accession} was null – skipping"
                )
                continue
            for metadatum in metadata_content:
                marker, created = SampleMetadataMarker.objects.update_or_create(
                    name=metadatum["marker"]["value"],
                    type=metadata_type,
                    defaults={"iri": metadatum["marker"]["iri"]},
                )
                if created:
                    logging.info(f"Created new SampleMetadataMarker {marker}")
                self.structured_metadata.update_or_create(
                    marker=marker,
                    defaults={
                        "source": SampleStructuredDatum.BIOSAMPLES,
                        "measurement": metadatum["measurement"]["value"],
                        "partner_name": metadatum.get("partner", {}).get("value"),
                        "partner_iri": metadatum.get("partner", {}).get("iri"),
                        "units": metadatum.get("measurement_units", {}).get("value"),
                    },
                )

        if checklist:
            checklist_metadata = checklist
        else:
            checklist_metadata = get_checklist_metadata(self.accession)

        for metadatum in checklist_metadata:
            marker, created = SampleMetadataMarker.objects.update_or_create(
                name=metadatum.tag, type="ENA Checklist"
            )
            if created:
                logging.info(f"Created new SampleMetadataMarker {marker}")
            self.structured_metadata.update_or_create(
                marker=marker,
                defaults={
                    "source": SampleStructuredDatum.ENA,
                    "measurement": metadatum.value,
                    "units": metadatum.units,
                },
            )

    def refresh_external_references(self, external_references_list: List[dict] = None):
        """
        Set the details on Sample, that come from biosamples External References.
        Either the biosamples externalReferences response section is provided,
        or optionally fetching that from the BioSamples API.
        :param external_references_list: Optional structure of `externalReferences` biosamples API response if already known.
        :return:
        """
        if not external_references_list:
            refs = get_biosample(self.accession).get("externalReferences")
        else:
            refs = external_references_list
        for ref in refs:
            if "MTBLS" in ref.get("url", ""):
                self.metabolights_study = f"MTBLS{ref['url'].split('MTBLS')[1]}"
                self.save()

    def get_metabolights_files(self):
        mtbls = self.metabolights_study
        if not mtbls:
            logging.info(f"No MTBLS accession is present in {self}")
            return
        assays = get_metabolights_assays(self.metabolights_study, self.accession)
        logging.info(assays)
        return assays
        # project_samples_files = get_metabolights_project_files(mtbls)
        # try:
        #     sample_files = next(
        #         files
        #         for sample, files in project_samples_files.items()
        #         if sample.lower() in [self.accession.lower(), self.title.lower()]
        #     )
        # except StopIteration:
        #     logging.warning(
        #         f"Sample {self} has metadata suggesting it is in {mtbls}. Yet no sample matched it in that project."
        #     )
        # else:
        #     self.metabolights_files = sample_files
        #     # self.has_metabolomics = True
        #     logging.info(
        #         f"Stored {len(sample_files)} metabolights filenames for {mtbls}"
        #     )
        #     self.save()


class SampleMetadataMarker(models.Model):
    """
    A metadata marker is a definition for measurements on an Animal or Sample.
    Often the definition is linked via an IRI to an ontology/controlled vocabulary.
    """

    name = models.CharField(max_length=100)
    iri = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ("type",)
        unique_together = [("name", "type")]

    def __str__(self):
        return f"Sample Metadata Marker {self.id}: {self.name} ({self.type})"


class StructuredDatumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("marker")


class AbstractStructuredDatum(models.Model):
    """
    An individual measurement on an Animal(-level Sample) or (extraction level-)Sample.
    Keyed to a SampleMetadataMarker.
    """

    ENA = "ena"
    BIOSAMPLES = "biosamples"
    SOURCE_CHOICES = [(ENA, ENA), (BIOSAMPLES, BIOSAMPLES)]

    source = models.CharField(choices=SOURCE_CHOICES, max_length=15)

    marker = models.ForeignKey(SampleMetadataMarker, on_delete=models.CASCADE)
    measurement = models.CharField(max_length=200)
    units = models.CharField(max_length=100, null=True, blank=True)

    partner_name = models.CharField(max_length=100, null=True, blank=True)
    partner_iri = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class SampleStructuredDatum(AbstractStructuredDatum):
    """
    An individual measurement on an (extraction level-)Sample.
    Keyed by a SampleMetadataMarker.
    """

    objects = StructuredDatumManager()

    sample = models.ForeignKey(
        Sample, on_delete=models.CASCADE, related_name="structured_metadata"
    )

    def __str__(self):
        return f"Sample {self.sample.accession} metadata {self.marker.id}: {self.marker.name}"

    class Meta:
        ordering = (
            "marker__type",
            "marker__name",
            "id",
        )


class AnimalStructuredDatum(AbstractStructuredDatum):
    """
    An individual measurement on an (animal level-)Sample.
    Keyed by a SampleMetadataMarker.
    """

    objects = StructuredDatumManager()

    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="structured_metadata"
    )

    def __str__(self):
        return f"Animal {self.animal.accession} metadata {self.marker.id}: {self.marker.name}"

    class Meta:
        ordering = (
            "marker__type",
            "marker__name",
            "id",
        )


class AnalysisSummary(models.Model):
    """
    A Markdown document describing some analysis performed by the collaboration,
    related to (e.g. using) other data types.
    """

    slug = models.SlugField(primary_key=True, max_length=200, unique=True)
    title = models.CharField(max_length=200)
    content = MartorField(
        help_text="Markdown document describing an analysis of one or more catalogues/samples"
    )
    samples = models.ManyToManyField(
        Sample, related_name="analysis_summaries", blank=True
    )
    genome_catalogues = models.ManyToManyField(
        "GenomeCatalogue", related_name="analysis_summaries", blank=True
    )
    viral_catalogues = models.ManyToManyField(
        "ViralCatalogue", related_name="analysis_summaries", blank=True
    )
    author = models.CharField(max_length=200)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slug} - {self.title}"

    def get_absolute_url(self):
        return reverse("analysis_summary_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "analysis summaries"
        permissions = [("publish_annotation", "Can publish an analysis summary")]


class GenomeCatalogue(models.Model):
    """
    A collection of draft genomes, as a subset of a "related mag catalogue", which is a MAG catalogue
    on MGnify (https://www.ebi.ac.uk/metagenomics)
    """

    id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=100)
    biome = models.CharField(max_length=200)
    related_mag_catalogue_id = models.CharField(max_length=100)
    system = models.CharField(choices=Animal.SYSTEM_CHOICES, max_length=10, null=False)


class Genome(models.Model):
    """
    A draft genome assembled from the metagenomic samples.
    Points to a genome accession on MGnify.
    """

    accession = models.CharField(primary_key=True, max_length=15)
    cluster_representative = models.CharField(max_length=15)
    catalogue = models.ForeignKey(
        GenomeCatalogue, on_delete=models.CASCADE, related_name="genomes"
    )
    taxonomy = models.CharField(max_length=200)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("accession",)


class ViralCatalogue(models.Model):
    """
    A collection of (probable) viral fragments detected in the metagenomic reads.
    """

    id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=100)
    biome = models.CharField(max_length=200)
    related_genome_catalogue = models.ForeignKey(
        GenomeCatalogue,
        null=True,
        blank=True,
        related_name="viral_catalogues",
        on_delete=models.SET_NULL,
    )
    system = models.CharField(choices=Animal.SYSTEM_CHOICES, max_length=10, null=False)


class ViralFragmentClusterManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(representative_of_cluster_size=models.Count("cluster_members"))
        )


class ViralFragment(models.Model):
    """
    A probable viral section of DNA found in a contig assembled from the metagenomic samples.
    If the fragment maps to a MAG Genome, that is also linked.
    Contig details are linked to the MGnify Analysis (MGYA) and contig.
    Fragment are clustered by nucleotide identity, so some are cluster representatives for others.
    """

    objects = ViralFragmentClusterManager()

    PROPHAGE = "prophage"
    PHAGE = "phage"
    VIRAL_TYPE_CHOICES = [(PHAGE, PHAGE), (PROPHAGE, PROPHAGE)]

    id = models.CharField(primary_key=True, max_length=100, verbose_name="ID")
    catalogue = models.ForeignKey(
        ViralCatalogue, on_delete=models.CASCADE, related_name="viral_fragments"
    )
    cluster_representative = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cluster_members",
    )
    contig_id = models.CharField(max_length=100, verbose_name="Contig ID")
    mgnify_analysis_accession = models.CharField(max_length=12)
    start_within_contig = models.IntegerField()
    end_within_contig = models.IntegerField()
    metadata = models.JSONField(default=dict, blank=True)
    host_mag = models.ForeignKey(
        Genome,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="viral_fragments",
        verbose_name="Host MAG",
    )
    viral_type = models.CharField(choices=VIRAL_TYPE_CHOICES, max_length=10)
    taxonomy = models.CharField(null=True, blank=True, max_length=100)

    gff = models.TextField(blank=True, default="")

    @property
    def is_cluster_representative(self):
        return self.cluster_representative is None
