import logging

from django.core.management.base import BaseCommand

from holofood.models import Sample, Project


class Command(BaseCommand):
    help = "(Re)fetch structureddata for all Samples, from the Biosamples API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--sample", type=str, help="Sample accession, if only one should be updated"
        )
        parser.add_argument(
            "--project",
            type=str,
            help="Project accession, if only one should be updated",
        )

    def handle(self, *args, **options):
        if options["sample"]:
            samples = [Sample.objects.get(accession=options["sample"])]
        elif options["project"]:
            samples = Project.objects.get(options["project"]).sample_set.all()
        else:
            samples = Sample.objects.all()

        for sample in samples:
            logging.info(f"Refreshing structureddata for sample {sample.accession}")
            sample.refresh_structureddata()

        self.stdout.write(self.style.SUCCESS(f"Done"))
