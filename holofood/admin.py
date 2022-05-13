from django.contrib import admin
from holofood.models import (
    Sample,
    Project,
    SampleMetadataMarker,
    SampleStructuredDatum,
    BiosamplesPartner,
)


class SampleMetadataInline(admin.TabularInline):
    model = SampleStructuredDatum


@admin.register(Project, SampleMetadataMarker, BiosamplesPartner, SampleStructuredDatum)
class GenericAdmin(admin.ModelAdmin):
    pass


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    inlines = [SampleMetadataInline]
