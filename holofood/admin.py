from django import forms
from django.contrib import admin
from django.db import models
from django_admin_inline_paginator.admin import TabularInlinePaginated

from holofood.models import (
    Sample,
    Project,
    SampleMetadataMarker,
    SampleStructuredDatum,
    SampleAnnotation,
    GenomeCatalogue,
    Genome,
    ViralFragment,
    ViralCatalogue,
)


class SampleMetadataInline(admin.TabularInline):
    model = SampleStructuredDatum


@admin.register(Project, SampleMetadataMarker, SampleStructuredDatum)
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


class GenomeInline(TabularInlinePaginated):
    model = Genome
    per_page = 5
    can_delete = True
    show_change_link = True
    show_full_result_count = True


@admin.register(GenomeCatalogue)
class GenomeCatalogueAdmin(admin.ModelAdmin):
    inlines = [GenomeInline]


class ViralFragmentInline(TabularInlinePaginated):
    model = ViralFragment
    fields = ["id", "cluster_representative", "viral_type"]
    per_page = 5
    can_delete = True
    show_change_link = True
    show_full_result_count = True


@admin.register(ViralCatalogue)
class ViralCatalogueAdmin(admin.ModelAdmin):
    inlines = [ViralFragmentInline]


@admin.register(ViralFragment)
class ViralFragmentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={"cols": 180, "style": "font-family: monospace;"}
            )
        },
        models.JSONField: {
            "widget": forms.Textarea(
                attrs={"cols": 180, "style": "font-family: monospace;"}
            )
        },
    }
