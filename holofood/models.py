import logging

from django.db import models
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.text import slugify
from martor.models import MartorField

from holofood.external_apis.biosamples.api import get_sample_structured_data
from holofood.external_apis.ena.submit_api import get_checklist_metadata
from holofood.utils import holofood_config


class Project(models.Model):
    accession = models.CharField(primary_key=True, max_length=15)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Project {self.accession} - {self.title}"


class SampleManager(models.Manager):
    def get_queryset(self):
        primary_markers = SampleStructuredDatum.objects.filter(
            marker__name__in=holofood_config.tables.samples_list.default_metadata_marker_columns
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

    def __str__(self):
        return f"Sample {self.accession} - {self.title}"

    class Meta:
        ordering = ("accession",)

    def refresh_structureddata(self):
        metadata = get_sample_structured_data(self.accession)

        for metadata_type, metadata_content in metadata.items():
            for metadatum in metadata_content:
                marker, created = SampleMetadataMarker.objects.update_or_create(
                    name=metadatum["marker"]["value"],
                    defaults={"iri": metadatum["marker"]["iri"], "type": metadata_type},
                )
                if created:
                    logging.info(f"Created new SampleMetadataMarker {marker.id}")
                if "partner" in metadatum:
                    partner, _ = BiosamplesPartner.objects.update_or_create(
                        name=metadatum["partner"]["value"],
                        defaults={"iri": metadatum["partner"]["iri"]},
                    )
                else:
                    partner = None
                self.structured_metadata.update_or_create(
                    marker=marker,
                    defaults={
                        "source": SampleStructuredDatum.BIOSAMPLES,
                        "measurement": metadatum["measurement"]["value"],
                        "partner": partner,
                        "units": metadatum.get("measurement_units", {}).get("value"),
                    },
                )

        checklist_metadata = get_checklist_metadata(self.accession)

        for metadatum in checklist_metadata:
            marker, created = SampleMetadataMarker.objects.update_or_create(
                name=metadatum.tag,
            )
            if created:
                logging.info(f"Created new SampleMetadataMarker {marker.id}")
            self.structured_metadata.update_or_create(
                marker=marker,
                defaults={
                    "source": SampleStructuredDatum.ENA,
                    "measurement": metadatum.value,
                    "units": metadatum.units,
                },
            )

        self.refresh_from_db()
        try:
            tax_id_data = self.structured_metadata.get(marker__name="host taxid")
            system = holofood_config.ena.systems[str(tax_id_data.measurement)]
        except (self.DoesNotExist, SampleMetadataMarker.DoesNotExist, KeyError) as e:
            logging.error(f"Error determining System for Sample {self.accession}")
            raise e
        logging.info(f"Setting system to {system} for sample {self.accession}")
        self.system = system
        self.save(update_fields=["system"])


class SampleMetadataMarker(models.Model):
    name = models.CharField(max_length=100)
    iri = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        ordering = ("type",)

    def __str__(self):
        return f"Sample Metadata Marker {self.id}: {self.name}"


class BiosamplesPartner(models.Model):
    name = models.CharField(max_length=100)
    iri = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Partner {self.id}: {self.name}"


class SampleStructuredDatumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("marker", "partner")


class SampleStructuredDatum(models.Model):
    objects = SampleStructuredDatumManager()

    ENA = "ena"
    BIOSAMPLES = "biosamples"
    SOURCE_CHOICES = [(ENA, ENA), (BIOSAMPLES, BIOSAMPLES)]

    sample = models.ForeignKey(
        Sample, on_delete=models.CASCADE, related_name="structured_metadata"
    )
    marker = models.ForeignKey(SampleMetadataMarker, on_delete=models.CASCADE)
    measurement = models.CharField(max_length=100)
    units = models.CharField(max_length=100, null=True)
    partner = models.ForeignKey(BiosamplesPartner, on_delete=models.CASCADE, null=True)
    source = models.CharField(choices=SOURCE_CHOICES, max_length=15)

    def __str__(self):
        return f"Sample {self.sample.accession} metadata {self.marker.id}: {self.marker.name}"

    class Meta:
        ordering = (
            "marker__type",
            "marker__name",
            "id",
        )


class SampleAnnotation(models.Model):
    slug = models.SlugField(primary_key=True, max_length=200, unique=True)
    title = models.CharField(max_length=200)
    content = MartorField(
        help_text="Markdown document describing an analysis of one or more projects/samples"
    )
    samples = models.ManyToManyField(Sample, related_name="annotations", blank=True)
    projects = models.ManyToManyField(Project, related_name="annotations", blank=True)
    author = models.CharField(max_length=200)
    created = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slug} - {self.title}"

    def get_absolute_url(self):
        return reverse("annotation_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        permissions = [("publish_annotation", "Can publish an annotation")]
