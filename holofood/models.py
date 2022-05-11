import logging

from django.db import models

from holofood.external_apis.biosamples.api import get_sample_structured_data
from holofood.external_apis.ena.submit_api import get_checklist_metadata


class Project(models.Model):
    accession = models.CharField(primary_key=True, max_length=15)
    title = models.CharField(max_length=200)


class SampleManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("project")
            .prefetch_related("structured_metadata", "structured_metadata__marker")
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

    class Meta:
        ordering = ("accession",)

    def refresh_structureddata(self):
        metadata = get_sample_structured_data(self.accession)

        for metadatum in metadata:
            marker, created = SampleMetadataMarker.objects.update_or_create(
                name=metadatum["marker"]["value"],
                defaults={"iri": metadatum["marker"]["iri"]},
            )
            if created:
                logging.info(f"Created new SampleMetadataMarker {marker.id}")
            partner, _ = BiosamplesPartner.objects.update_or_create(
                name=metadatum["partner"]["value"],
                defaults={"iri": metadatum["partner"]["iri"]},
            )
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


class SampleMetadataMarker(models.Model):
    name = models.CharField(max_length=100)
    iri = models.CharField(max_length=100, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]


class BiosamplesPartner(models.Model):
    name = models.CharField(max_length=100)
    iri = models.CharField(max_length=100, null=True)


# class SampleStructuredDatumManager(models.Manager):
#     def get_queryset(self):
#         return (
#             super()
#             .get_queryset()
#             .select_related("marker")
# .prefetch_related("structured_metadata")
# )


class SampleStructuredDatum(models.Model):
    # objects = SampleStructuredDatumManager()

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
