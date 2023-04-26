import logging

from django.core.management.base import BaseCommand

from holofood.models import Sample, Animal


class Command(BaseCommand):
    help = "(Re)fetch external data for some or all Samples/Animals, from BioSamples."

    def add_arguments(self, parser):
        parser.add_argument(
            "--samples",
            type=str,
            help="Sample accessions to update. Overrides `--sample_filters`. Use 'ALL' for all.",
            nargs="+",
            metavar="ACCESSION",
        )
        parser.add_argument(
            "--animals",
            type=str,
            help="Animals accessions to update. Overrides `--animal_filters`. Use 'ALL' for all.",
            nargs="+",
            metavar="ACCESSION",
        )
        parser.add_argument(
            "--sample_filters",
            type=str,
            help="Sample filter as Django-esque query expressions e.g. accession__gt=SAMEA002",
            nargs="+",
            metavar="FILTER",
        )
        parser.add_argument(
            "--animal_filters",
            type=str,
            help="Animal filter as Django-esque query expressions e.g. accession__gt=SAMEA002",
            nargs="+",
            metavar="FILTER",
        )

    def handle(self, *args, **options):
        samples = None
        if options["samples"]:
            if "ALL" in options["samples"]:
                samples = Sample.objects.all()
            else:
                samples = Sample.objects.filter(accession__in=options["samples"])
        if options["sample_filters"]:
            filters = dict(tuple(f.split("=")) for f in options["sample_filters"])
            samples = Sample.objects.filter(**filters)
        if samples:
            logging.info(f"Fetching metadata for {samples.count()} samples")
            for sample in samples:
                sample.refresh_structureddata()
            self.stdout.write(self.style.SUCCESS(f"Done for samples"))

        animals = None
        if options["animals"]:
            if "ALL" in options["animals"]:
                animals = Animal.objects.all()
            else:
                animals = Animal.objects.filter(accession__in=options["animals"])
        if options["animal_filters"]:
            filters = dict(tuple(f.split("=")) for f in options["animal_filters"])
            animals = Animal.objects.filter(**filters)
        if animals:
            logging.info(f"Fetching metadata for {animals.count()} animals")
            for animal in animals:
                animal.refresh_structureddata()
            self.stdout.write(self.style.SUCCESS(f"Done for animals"))
