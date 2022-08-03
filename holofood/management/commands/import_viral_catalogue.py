import argparse
import logging
import os
import pathlib
from csv import DictReader

from django.core.management.base import BaseCommand, CommandError

from holofood.models import ViralCatalogue, GenomeCatalogue


class DirFileType:
    def __call__(self, path):
        if os.path.isdir(path):
            return pathlib.Path(path)
        else:
            raise argparse.ArgumentTypeError(f"{path} is not a Directory")


class Command(BaseCommand):
    help = "Import a viral catalogue, from a TSV file listing fragments and GFF files of the viral annotations."

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
            "gffs_dir",
            type=DirFileType(),
            help="Path to a directory containing GFFs for each sequence, each named {sequence_id}.gff",
        )
        parser.add_argument(
            "title",
            type=str,
            help="Title of the catalogue",
        )
        parser.add_argument(
            "related_mag_catalogue_id",
            type=str,
            help="ID of the related MAG catalogue in the HoloFood database",
        )
        parser.add_argument(
            "--biome",
            type=str,
            help="Biome of the catalogue (or None to copy from related MAG catalogue)",
            default=None,
        )
        parser.add_argument(
            "--system",
            type=str,
            help="System (chicken/salmon) of the catalogue (or None to copy from related MAG catalogue)",
            default=None,
        )

    def handle(self, *args, **options):
        tsv_file = options["catalogue_file"]

        try:
            mag_catalogue = GenomeCatalogue.objects.get(
                id=options["related_mag_catalogue_id"]
            )
        except GenomeCatalogue.DoesNotExist:
            raise CommandError(
                f"Mag Catalogue {options['related_mag_catalogue_id']} does not yet exist."
            )

        logging.info(f"Related MAG catalogue is {mag_catalogue}")

        biome = options["biome"] or mag_catalogue.biome
        logging.info(f"Setting {biome=}")

        system = options["system"] or mag_catalogue.system
        logging.info(f"Setting {system=}")

        reader = DictReader(tsv_file, delimiter="\t")
        column_mapping = {
            "sequence_id": "id",
            "sequence_start": "start_within_contig",
            "sequence_end": "end_within_contig",
            "cluster_representative": "cluster_representative_id",
            "mgya": "mgnify_analysis_accession",
            "host_mgyg": "host_mag_id",
            "viral_type": "viral_type",
            "contig": "contig_id",
        }
        missing = set(column_mapping.keys()).difference(reader.fieldnames)
        if missing:
            raise CommandError(
                f"Not all expected columns were found in the TSV. {missing=}"
            )

        catalogue = ViralCatalogue.objects.create(
            id=options["catalogue_id"],
            title=options["title"],
            related_genome_catalogue=mag_catalogue,
            biome=biome,
            system=system,
        )
        logging.info(f"Created viral {catalogue=}")

        for sequence in reader:
            vir_data = {
                field_name: sequence[col_name]
                for col_name, field_name in column_mapping.items()
                if sequence[col_name] != ""
            }
            gff_path: pathlib.Path = (
                options["gffs_dir"] / f'{sequence["sequence_id"]}.gff'
            )

            if not gff_path.is_file():
                raise CommandError(f"No GFF file found for {sequence['sequence_id']}")
            with open(
                options["gffs_dir"] / f'{sequence["sequence_id"]}.gff', "r"
            ) as gff_stream:
                gff = gff_stream.read()

            frag = catalogue.viral_fragments.create(
                catalogue=catalogue, gff=gff, **vir_data
            )
            logging.debug(f"Created viral sequence {frag}")
        tsv_file.close()
        self.stdout.write(self.style.SUCCESS(f"Done"))
