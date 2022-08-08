import logging

from django.core.management.base import BaseCommand

from holofood.models import Sample

METADATA = "METADATA"
METAGENOMIC = "METAGENOMIC"


class Command(BaseCommand):
    help = "(Re)fetch external data for some or all Samples, from external APIs like BioSamples and MGnify"

    def add_arguments(self, parser):
        parser.add_argument(
            "--samples",
            type=str,
            help="Sample accessions, if only some should be updated",
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

    def handle(self, *args, **options):
        samples = None
        if options["samples"]:
            samples = Sample.objects.filter(accession__in=options["samples"])
        elif options["projects"]:
            samples = Sample.objects.filter(project__accession__in=options["projects"])
        samples = samples or Sample.objects
        if options["sample_filters"]:
            print(options["sample_filters"])
            filters = dict(tuple(f.split("=")) for f in options["sample_filters"])
            samples = samples.filter(**filters)
        samples = samples.all()

        for sample in samples:
            logging.info(f"Refreshing external data for sample {sample.accession}")
            if METADATA in options["types"]:
                logging.info(f"Refreshing structureddata for sample {sample.accession}")
                sample.refresh_structureddata()
            if METAGENOMIC in options["types"]:
                logging.info(
                    f"Refreshing metagenomics data for sample {sample.accession}"
                )
                sample.refresh_metagenomics_metadata()

        self.stdout.write(self.style.SUCCESS(f"Done"))
