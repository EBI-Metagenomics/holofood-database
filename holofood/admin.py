from django.contrib import admin

from holofood.models import (
    Sample,
    Project,
    SampleMetadataMarker,
    SampleStructuredDatum,
    BiosamplesPartner,
    SampleAnnotation,
)


class SampleMetadataInline(admin.TabularInline):
    model = SampleStructuredDatum


@admin.register(Project, SampleMetadataMarker, BiosamplesPartner, SampleStructuredDatum)
class GenericAdmin(admin.ModelAdmin):
    pass


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    inlines = [SampleMetadataInline]


@admin.register(SampleAnnotation)
class SampleAnnotationAdmin(admin.ModelAdmin):
    readonly_fields = ["created", "updated"]
    filter_horizontal = (
        "samples",
        "projects",
    )
