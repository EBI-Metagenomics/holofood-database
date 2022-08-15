import logging

from django.core.management.base import BaseCommand

from holofood.models import Sample, Project

METADATA = "METADATA"
METAGENOMIC = "METAGENOMIC"


class Command(BaseCommand):
    help = "(Re)fetch external data for some or all Samples, from external APIs like BioSamples and MGnify"

    def add_arguments(self, parser):
        parser.add_argument(
            "--samples",
            type=str,
            help="Sample accessions, if only some should be updated. Overrides `--projects` and `--sample_filters`.",
            nargs="+",
            metavar="ACCESSION",
        )
        parser.add_argument(
            "--projects",
            type=str,
            help="Project accessions, if only some should be updated",
            nargs="+",
            metavar="ACCESSION",
        )
        parser.add_argument(
            "--types",
            type=str,
            help=f"Which data types to fetch: {[METADATA, METAGENOMIC]}",
            nargs="+",
            metavar="DATATYPE",
            choices=[METADATA, METAGENOMIC],
            default=[METADATA, METAGENOMIC],
        )
        parser.add_argument(
            "--sample_filters",
            type=str,
            help="Sample filter as Django-esque query expressions e.g. accession__gt=SAMEA002",
            nargs="+",
            metavar="FILTER",
        )

    @staticmethod
    def _refresh_sample(sample: Sample, options: dict):
        logging.info(f"Refreshing external data for sample {sample.accession}")
        if METADATA in options["types"]:
            logging.info(f"Refreshing structureddata for sample {sample.accession}")
            sample.refresh_structureddata()
        if METAGENOMIC in options["types"]:
            logging.info(f"Refreshing metagenomics data for sample {sample.accession}")
            sample.refresh_metagenomics_metadata()

    @staticmethod
    def _refresh_project(project: Project, options: dict):
        if METADATA in options["types"]:
            logging.info(f"Refreshing structureddata for project {project.accession}")
            for sample in project.sample_set.all():
                sample.refresh_structureddata()
        if METAGENOMIC in options["types"]:
            logging.info(
                f"Refreshing metagenomics data for samples in project {project.accession}"
            )
            project.refresh_metagenomics_metadata()

    def handle(self, *args, **options):
        if options["samples"]:
            # Specific samples so call APIs one by one
            samples = Sample.objects.filter(accession__in=options["samples"])
            logging.info(
                f"Fetching metadata sample by sample for {samples.count()} samples"
            )
            for sample in samples:
                self._refresh_sample(sample, options)
            return self.stdout.write(self.style.SUCCESS(f"Done"))

        # Call APIs on a per-project basis if possible
        if options["projects"]:
            projects = Project.objects.filter(accession__in=options["projects"])
        else:
            projects = Project.objects

        if options["sample_filters"]:
            # Call APIs per-sample, filtering by project and user-defined filters
            filters = dict(tuple(f.split("=")) for f in options["sample_filters"])
            samples = Sample.objects.filter(**filters).filter(project__in=projects)
            for sample in samples:
                self._refresh_sample(sample, options)
            return self.stdout.write(self.style.SUCCESS(f"Done"))

        else:
            # Call APIs per-project
            for project in projects:
                self._refresh_project(project, options)
        self.stdout.write(self.style.SUCCESS(f"Done"))
