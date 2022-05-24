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
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        "title",
        "author",
        "slug",
        "content",
        "samples",
        "projects",
        "created",
        "updated",
        "is_published",
    )
    filter_horizontal = (
        "samples",
        "projects",
    )

    def changeform_view(self, request, *args, **kwargs):
        self.readonly_fields = list(self.readonly_fields)
        if not request.user.is_superuser:
            self.readonly_fields = ["created", "updated", "is_published"]

        return super().changeform_view(request, *args, **kwargs)
