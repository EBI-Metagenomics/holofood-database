import logging

from django.db import models
from django.db.models import Prefetch, Q
from django.urls import reverse
from django.utils.text import slugify
from martor.models import MartorField

from holofood.external_apis.biosamples.api import get_sample_structured_data
from holofood.external_apis.ena.browser_api import get_checklist_metadata
from holofood.external_apis.metabolights.api import get_metabolights_project_files
from holofood.external_apis.mgnify.api import MgnifyApi
from holofood.utils import holofood_config

_mgnify = MgnifyApi()


class Project(models.Model):
    accession = models.CharField(primary_key=True, max_length=15)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Project {self.accession} - {self.title}"

    def refresh_metagenomics_metadata(self):
        logging.info(
            f"Checking metagenomics data existence for samples in project {self}"
        )
        mgnify_samples = _mgnify.get_metagenomics_samples_for_project(self.accession)
        samples_to_update = self.sample_set.filter(accession__in=mgnify_samples)
        samples_to_update.update(has_metagenomics=True)
        logging.info(
            f"Project {self} has {len(mgnify_samples)} samples with metagenomics data."
        )

    def refresh_metabolomics_metadata(self):
        logging.info(f"Checking metabolomics data files for sample in project {self}")
        metabolights_projects = (
            SampleStructuredDatum.objects.filter(
                sample__project_id=self.pk,
                marker__name=holofood_config.metabolights.metabolights_accession_marker_in_biosamples,
            )
            .order_by("measurement")
            .values_list("measurement", flat=True)
            .distinct()
        )
        logging.info(
            f"Project {self} contains samples with metabolights projects: {metabolights_projects}"
        )
        for mtbls in metabolights_projects:
            logging.info(f"Matching samples for {mtbls=} to project {self}")
            samples_updated_count = 0
            for sample_id, files in get_metabolights_project_files(mtbls).items():
                sample = self.sample_set.filter(
                    Q(accession__iexact=sample_id) | Q(title__iexact=sample_id)
                ).first()
                if sample:
                    sample.metabolights_files = files
                    sample.has_metabolomics = True
                    sample.save()
                    logging.info(f"Update metabolomics files for sample {sample}")
                    samples_updated_count += 1
                else:
                    logging.warning(
                        f"Project {self} did not contain a sample for MTBLS project {mtbls}'s sample {sample_id}"
                    )
            logging.info(
                f"Updated metabolights for {samples_updated_count} samples from {mtbls}"
            )


class SampleManager(models.Manager):
    def get_queryset(self):
        prefetchable_markers = (
            holofood_config.tables.samples_list.default_metadata_marker_columns
            + [holofood_config.metabolights.metabolights_accession_marker_in_biosamples]
        )
        primary_markers = SampleStructuredDatum.objects.filter(
            marker__name__in=prefetchable_markers
        )
        return (
            super()
            .get_queryset()
            .select_related("project")
            .prefetch_related(
                Prefetch(
                    "structured_metadata",
                    queryset=primary_markers,
                    to_attr="primary_metadata",
                )
            )
        )


class Sample(models.Model):
    objects = SampleManager()

    CHICKEN = "chicken"
    SALMON = "salmon"
    SYSTEM_CHOICES = [(CHICKEN, CHICKEN), (SALMON, SALMON)]

    accession = models.CharField(primary_key=True, max_length=15)
    system = models.CharField(choices=SYSTEM_CHOICES, max_length=10, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    animal_code = models.CharField(max_length=20)

    has_metagenomics = models.BooleanField(default=False)
    has_metabolomics = models.BooleanField(default=False)

    ena_run_accessions = models.JSONField(default=list, blank=True)
    metabolights_files = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Sample {self.accession} - {self.title}"

    class Meta:
        ordering = ("accession",)

    def refresh_structureddata(self):
        metadata = get_sample_structured_data(self.accession)

        for metadata_type, metadata_content in metadata.items():
            if not metadata_content:
                logging.warning(
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

        self.refresh_from_db()
        tax_id_data = self.structured_metadata.filter(marker__name="host taxid").first()
        if not tax_id_data:
            raise Exception(f"Error determining System for Sample {self.accession}")
        try:
            system = holofood_config.ena.systems[str(tax_id_data.measurement)]
        except KeyError as e:
            logging.error(f"Error determining System for Sample {self.accession}")
            raise e
        logging.info(f"Setting system to {system} for sample {self.accession}")
        self.system = system

        animal_code = self.structured_metadata.filter(
            marker__name="host subject id"
        ).first()
        if not animal_code:
            raise Exception(
                f"Error determining animal code for Sample {self.accession}"
            )
        self.animal_code = animal_code.measurement

        self.save(update_fields=["system"])

    def refresh_metagenomics_metadata(self):
        logging.debug(f"Checking metagenomics data existence for sample {self}")
        self.has_metagenomics = _mgnify.get_metagenomics_existence_for_sample(
            self.accession
        )
        logging.debug(f"Sample {self} has metagenomics data? {self.has_metagenomics}")
        self.save()

    @property
    def metabolights_project(self) -> str:
        if hasattr(self, "primary_metadata"):
            # Use the prefetched values for efficiency
            try:
                mtbls_metadatum: SampleStructuredDatum = next(
                    metadatum
                    for metadatum in self.primary_metadata
                    if metadatum.marker.name
                    == holofood_config.metabolights.metabolights_accession_marker_in_biosamples
                )
            except StopIteration:
                logging.debug(f"No metabolights project for {self}")
            else:
                return mtbls_metadatum.measurement
        else:
            logging.warning(
                "No primary_metadata attribute available on sample. Model manager skipped?"
            )
            mtbls_metadatum = self.structured_metadata.filter(
                marker__name=holofood_config.metabolights.metabolights_accession_marker_in_biosamples
            ).first()
            if mtbls_metadatum:
                return mtbls_metadatum.measurement

    def refresh_metabolomics_metadata(self):
        mtbls = self.metabolights_project
        if not mtbls:
            logging.info(f"No MTBLS accession is present in metadata of {self}")
            return
        logging.debug(f"Refreshing metabolomics data for {self}: {mtbls}")
        project_samples_files = get_metabolights_project_files(mtbls)
        try:
            sample_files = next(
                files
                for sample, files in project_samples_files.items()
                if sample.lower() in [self.accession.lower(), self.title.lower()]
            )
        except StopIteration:
            logging.warning(
                f"Sample {self} has metadata suggesting it is in {mtbls}. Yet no sample matched it in that project."
            )
        else:
            self.metabolights_files = sample_files
            self.has_metabolomics = True
            logging.info(
                f"Stored {len(sample_files)} metabolights filenames for {mtbls}"
            )
            self.save()


class SampleMetadataMarker(models.Model):
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


class SampleStructuredDatumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("marker")


class SampleStructuredDatum(models.Model):
    objects = SampleStructuredDatumManager()

    ENA = "ena"
    BIOSAMPLES = "biosamples"
    SOURCE_CHOICES = [(ENA, ENA), (BIOSAMPLES, BIOSAMPLES)]

    sample = models.ForeignKey(
        Sample, on_delete=models.CASCADE, related_name="structured_metadata"
    )
    marker = models.ForeignKey(SampleMetadataMarker, on_delete=models.CASCADE)
    measurement = models.CharField(max_length=200)
    units = models.CharField(max_length=100, null=True, blank=True)

    partner_name = models.CharField(max_length=100, null=True, blank=True)
    partner_iri = models.CharField(max_length=100, null=True, blank=True)

    source = models.CharField(choices=SOURCE_CHOICES, max_length=15)

    def __str__(self):
        return f"Sample {self.sample.accession} metadata {self.marker.id}: {self.marker.name}"

    class Meta:
        ordering = (
            "marker__type",
            "marker__name",
            "id",
        )


class AnalysisSummary(models.Model):
    slug = models.SlugField(primary_key=True, max_length=200, unique=True)
    title = models.CharField(max_length=200)
    content = MartorField(
        help_text="Markdown document describing an analysis of one or more projects/samples"
    )
    samples = models.ManyToManyField(
        Sample, related_name="analysis_summaries", blank=True
    )
    projects = models.ManyToManyField(
        Project, related_name="analysis_summaries", blank=True
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
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=100)
    biome = models.CharField(max_length=200)
    related_mag_catalogue_id = models.CharField(max_length=100)
    system = models.CharField(choices=Sample.SYSTEM_CHOICES, max_length=10, null=False)


class Genome(models.Model):
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
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=100)
    biome = models.CharField(max_length=200)
    related_genome_catalogue = models.ForeignKey(
        GenomeCatalogue,
        null=True,
        blank=True,
        related_name="viral_catalogues",
        on_delete=models.SET_NULL,
    )
    system = models.CharField(choices=Sample.SYSTEM_CHOICES, max_length=10, null=False)


class ViralFragmentClusterManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(representative_of_cluster_size=models.Count("cluster_members"))
        )


class ViralFragment(models.Model):
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
