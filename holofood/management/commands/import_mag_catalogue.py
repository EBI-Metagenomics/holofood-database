import argparse
import logging
import re
from csv import DictReader

from django.core.management.base import BaseCommand, CommandError

from holofood.models import GenomeCatalogue


class Command(BaseCommand):
    help = "Import a MAG catalogue, from a TSV file listing the MAGs and their species reps."

    def add_arguments(self, parser):
        parser.add_argument(
            "catalogue_id",
            type=str,
            help="ID of the catalogue, in slug form.",
        )
        parser.add_argument(
            "catalogue_file",
            type=argparse.FileType("r"),
            help="Path to the TSV file listing viral sequences",
        )
        parser.add_argument(
            "title",
            type=str,
            help="Title of the catalogue",
        )
        parser.add_argument(
            "related_mag_catalogue_id",
            type=str,
            help="ID of the related public MAG catalogue on MGnify",
        )
        parser.add_argument(
            "biome",
            type=str,
            help="Biome of the catalogue (or None to copy from related MAG catalogue)",
        )
        parser.add_argument(
            "system",
            type=str,
            help="System (chicken/salmon) of the catalogue (or None to copy from related MAG catalogue)",
        )

    @staticmethod
    def _parse_taxonomic_lineage(lineage_string: str) -> str:
        if lineage_string.startswith("d__"):
            return (
                re.sub("(;?[a-z]__)", " > ", lineage_string)
                .strip()
                .lstrip("> ")
                .rstrip("> ")
            )
        return lineage_string

    def handle(self, *args, **options):
        tsv_file = options["catalogue_file"]

        reader = DictReader(tsv_file, delimiter="\t")

        column_mapping = {
            "Genome": "accession",
            "Species_rep": "cluster_representative",
            "Lineage": "taxonomy",
        }

        missing = set(column_mapping.keys()).difference(reader.fieldnames)
        if missing:
            raise CommandError(
                f"Not all expected columns were found in the TSV. {missing=}"
            )

        catalogue = GenomeCatalogue.objects.create(
            id=options["catalogue_id"],
            title=options["title"],
            related_mag_catalogue_id=options["related_mag_catalogue_id"],
            biome=options["biome"],
            system=options["system"],
        )
        logging.info(f"Created MAG {catalogue=}")
        for mag in reader:
            mag_data = {
                field_name: mag[col_name]
                for col_name, field_name in column_mapping.items()
                if mag[col_name] != ""
            }
            if "taxonomy" in mag_data:
                mag_data["taxonomy"] = self._parse_taxonomic_lineage(
                    mag_data["taxonomy"]
                )

            metadata = {
                col_name: col_val
                for col_name, col_val in mag.items()
                if col_name not in column_mapping
            }

            genome = catalogue.genomes.create(
                catalogue=catalogue, **mag_data, metadata=metadata
            )
            logging.debug(f"Created genome {genome}")
        tsv_file.close()
        self.stdout.write(self.style.SUCCESS(f"Done"))
