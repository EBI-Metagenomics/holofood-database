import argparse
import logging
from csv import DictReader

from django.core.management.base import BaseCommand, CommandError

from holofood.models import ViralCatalogue, GenomeCatalogue


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
            "gff_file",
            type=argparse.FileType("r"),
            help="Path to the GFF file with annotations for contigs in the catalogue",
        )
        parser.add_argument(
            "--title",
            type=str,
            help="Title of the catalogue. Must be provided if catalogue does not yet exist.",
            default=None,
        )
        parser.add_argument(
            "--related_mag_catalogue_id",
            type=str,
            help="ID of the related MAG catalogue in the HoloFood database. Must be provided if catalogue does not yet exist.",
            default=None,
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
        gff_file = options["gff_file"]

        existing_catalogue = ViralCatalogue.objects.filter(id=options["catalogue_id"])

        if not existing_catalogue.exists():
            if not options["title"]:
                raise CommandError(
                    f"--title must be provided since catalogue does not yet exist"
                )

            if not options["related_mag_catalogue_id"]:
                raise CommandError(
                    f"--related_mag_catalogue_id must be provided since catalogue does not yet exist"
                )

            try:
                mag_catalogue = GenomeCatalogue.objects.get(
                    id=options["related_mag_catalogue_id"]
                )
            except GenomeCatalogue.DoesNotExist:
                raise CommandError(
                    f"Mag Catalogue {options['related_mag_catalogue_id']} does not yet exist."
                )
        else:
            mag_catalogue = existing_catalogue.first().related_genome_catalogue

        logging.info(f"Related MAG catalogue is {mag_catalogue}")

        biome = options["biome"] or mag_catalogue.biome
        logging.info(f"Setting {biome=}")

        system = options["system"] or mag_catalogue.system
        logging.info(f"Setting {system=}")

        tsv_reader = DictReader(tsv_file, delimiter="\t")
        column_mapping = {
            "sequence_id": "id",
            "sequence_start": "start_within_contig",
            "sequence_end": "end_within_contig",
            "cluster_representative": "cluster_representative_id",
            "mgya": "mgnify_analysis_accession",
            "viral_type": "viral_type",
            "contig": "contig_id",
            "viral_taxonomy": "taxonomy",
        }
        missing = set(column_mapping.keys()).difference(tsv_reader.fieldnames)
        if missing:
            raise CommandError(
                f"Not all expected columns were found in the TSV. {missing=}"
            )

        catalogue, created = ViralCatalogue.objects.get_or_create(
            id=options["catalogue_id"],
            defaults={
                "title": options["title"],
                "related_genome_catalogue": mag_catalogue,
                "biome": biome,
                "system": system,
            },
        )
        if created:
            logging.info(f"Created viral {catalogue=}")
        else:
            logging.info(f"Adding sequences to existing viral {catalogue=}")

        annotations_per_contig = {}
        for annotation in gff_file:
            contig_id = annotation.split()[0]
            annotations_per_contig.setdefault(contig_id, []).append(annotation.strip())

        for sequence in tsv_reader:
            vir_data = {
                field_name: sequence[col_name]
                for col_name, field_name in column_mapping.items()
                if sequence[col_name] != ""
            }
            if "taxonomy" in vir_data:
                vir_data["taxonomy"] = (
                    vir_data["taxonomy"]
                    .replace(";", " > ")
                    .strip()
                    .lstrip(" >")
                    .rstrip(" >")
                )

            contig_id = sequence["contig"]

            gff = "\n".join(annotations_per_contig.get(contig_id, []))

            frag = catalogue.viral_fragments.create(
                catalogue=catalogue, gff=gff, **vir_data
            )
            logging.debug(f"Created viral sequence {frag}")
        tsv_file.close()
        self.stdout.write(self.style.SUCCESS(f"Done"))
