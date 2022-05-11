from django.contrib import admin
from holofood.models import (
    Sample,
    Project,
    SampleMetadataMarker,
    SampleStructuredDatum,
    BiosamplesPartner,
)


@admin.register(
    Sample, Project, SampleMetadataMarker, BiosamplesPartner, SampleStructuredDatum
)
class SampleAdmin(admin.ModelAdmin):
    pass
