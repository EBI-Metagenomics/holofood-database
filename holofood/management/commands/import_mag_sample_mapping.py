import argparse
import logging
from csv import DictReader

from django.core.management.base import BaseCommand, CommandError

from holofood.models import GenomeSampleContainment, Genome, Sample


class Command(BaseCommand):
    help = (
        "Import mappings between MAGs and samples, from a TSV file. "
        "Needs columns of at least `mgyg`, `sample_accession`, `containment`."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "mapping_file",
            type=argparse.FileType("r"),
            help="Path to the TSV file listing MAG – Sample pairs.",
        )
        parser.add_argument(
            "--catalogue_id_to_preclear",
            type=str,
            help="(Optional) ID of a MAG catalogue, in slug form, "
            "to clear all sample maps from prior to inserting new ones.",
            default=None,
        )

    def handle(self, *args, **options):
        tsv_file = options["mapping_file"]
        catalogue_id_to_preclear = options["catalogue_id_to_preclear"]

        if catalogue_id_to_preclear:
            existing_containments = GenomeSampleContainment.objects.filter(
                genome__catalogue_id=catalogue_id_to_preclear
            )
            logging.info(
                f"Deleting {existing_containments.count()} existing containments from genomes in {catalogue_id_to_preclear}"
            )
            existing_containments.delete()

        reader = DictReader(tsv_file, delimiter="\t")

        column_mapping = {
            "mgyg": "genome_id",
            "containment": "containment",
            "sample_accession": "sample_id",
        }

        missing = set(column_mapping.keys()).difference(reader.fieldnames)
        if missing:
            raise CommandError(
                f"Not all expected columns were found in the TSV. {missing=}"
            )

        for mapping in reader:
            logging.info(
                f"Importing mapping for {mapping['mgyg']} to sample {mapping['sample_accession']}"
            )
            try:
                sample = Sample.objects.get(accession=mapping["sample_accession"])
            except Sample.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Sample {mapping['sample_accession']} does not exist."
                    )
                )
                continue

            genomes = Genome.objects.filter(cluster_representative=mapping["mgyg"])
            if not genomes.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Genomes with cluster rep {mapping['mgyg']} do not exist."
                    )
                )
            else:
                logging.debug(f"Found {genomes.count()} Genomes")
            for genome in genomes:
                (
                    genome_sample_containment,
                    created,
                ) = GenomeSampleContainment.objects.get_or_create(
                    genome=genome,
                    sample=sample,
                    defaults={"containment": mapping["containment"]},
                )
            if created:
                logging.debug(
                    f"Created genome-sample-containment {genome_sample_containment}"
                )
            else:
                if mapping["containment"] > genome_sample_containment.containment:
                    logging.info(
                        f"Genome-sample-containment {genome_sample_containment} already exists, but updating "
                    )
                    logging.debug(
                        f"Updated genome-sample-containment {genome_sample_containment}"
                    )
        tsv_file.close()
        self.stdout.write(self.style.SUCCESS(f"Done"))
