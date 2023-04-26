import logging
from typing import Optional

from django.core.management.base import BaseCommand, CommandError

from holofood.external_apis.biosamples.api import get_project_samples
from holofood.models import Animal, Sample
from holofood.utils import holofood_config


class Command(BaseCommand):
    help = "(Re)fetches the list of Holofood samples from the BioSamples API."

    def add_arguments(self, parser):
        parser.add_argument(
            "--project_attr",
            type=str,
            help="Value of `project` attribute to search for in BioSamples",
            default="HoloFood",
        )
        parser.add_argument(
            "--webin_filter",
            type=str,
            help="Webin submitter accounts to include samples from. Others are filtered out.",
            nargs="+",
            metavar="WEBIN",
            default=["Webin-40894", "Webin-51990"],
        )
        parser.add_argument(
            "--biosamples_page_cursor",
            type=str,
            help="Pagination cursor value for biosamples, useful to continue running from a page other than the first.",
            default=None,
        )
        parser.add_argument(
            "--max_pages",
            type=int,
            help="Maximum page count to retrieve from biomsamples",
            default=None,
        )
        parser.add_argument(
            "--updated_since",
            type=str,
            help="ISO8601 formatted datetime, to limit samples to those updated since a certain date. E.g. 2023-04-31",
            default=None,
        )

    @staticmethod
    def is_animal(sample: dict) -> bool:
        for relationship in sample.get("relationships", []):
            if relationship.get("type") == "DERIVED_FROM" and relationship.get(
                "source"
            ) == sample.get("accession"):
                return False
        return True

    @staticmethod
    def get_system(sample: dict) -> Optional[str]:
        for system_characteristic in ["host tax id", "host taxid", "Organism"]:
            characteristic_value = Command.get_from_characteristics(
                sample, system_characteristic
            )
            system = holofood_config.ena.systems.get(characteristic_value)
            if system:
                return system
        return None

    @staticmethod
    def get_parent_animal(sample: dict) -> Optional[str]:
        try:
            parent = next(
                rel
                for rel in sample.get("relationships")
                if rel.get("type") == "DERIVED_FROM"
            )
        except StopIteration:
            return None
        return parent.get("target")

    @staticmethod
    def get_from_structured_data(
        sample: dict, section_type: str, marker: str
    ) -> Optional[str]:
        sections = sample.get("structuredData", [])
        try:
            section = next(sec for sec in sections if sec.get("type") == section_type)
        except StopIteration:
            return None
        try:
            metadatum = next(
                m for m in section["content"] if m.get("marker").get("value") == marker
            )
        except StopIteration:
            return None
        return metadatum.get("measurement").get("value")

    @staticmethod
    def get_from_characteristics(
        sample: dict, characteristic: str, raise_if_none: bool = False
    ) -> Optional[str]:
        try:
            char_value = (
                sample.get("characteristics", {}).get(characteristic, [])[0].get("text")
            )
        except IndexError:
            if raise_if_none:
                raise CommandError(
                    f"Could not get {characteristic =} for {sample.get('accession')}"
                )
        else:
            if raise_if_none and char_value is None:
                raise CommandError(
                    f"Could not get {characteristic =} for {sample.get('accession')}"
                )
            return char_value

    @staticmethod
    def get_sample_type(sample: dict) -> Optional[str]:
        experiment_type = Command.get_from_structured_data(
            sample, "SAMPLE", "Experiment"
        )
        if not experiment_type:
            logging.warning(
                f"No experiment type in metadata for {sample.get('accession')}"
            )
            return
        experiment_type = experiment_type.lower()

        if experiment_type in ["metagenomic", "metagenomics"]:
            return Sample.METAGENOMIC_ASSEMBLY
        if experiment_type == "amplicon":
            return Sample.METAGENOMIC_AMPLICON
        if experiment_type == "transcriptomics":
            return Sample.TRANSCRIPTOMIC
        if experiment_type == "metatranscriptomics":
            return Sample.META_TRANSCRIPTOMIC
        if experiment_type == "genomics":
            return Sample.HOST_GENOMIC
        if experiment_type == "ntm":
            return Sample.METABOLOMIC
        if experiment_type == "fatty_acids":
            return Sample.FATTY_ACIDS
        if experiment_type == "iodine":
            return Sample.IODINE
        if experiment_type == "heavy_metals":
            return Sample.HEAVY_METALS
        if experiment_type == "histology":
            return Sample.HISTOLOGICAL
        if experiment_type == "tm":
            return Sample.METABOLOMIC_TARGETED
        if experiment_type == "inflammatory_markers":
            return Sample.INFLAMMATORY_MARKERS

        else:
            logging.warning(
                f"Could not determine experiment/sample type for {sample.get('accession')}"
            )

    @staticmethod
    def characteristics_to_checklist_obj(sample: dict):
        characteristics = sample.get("characteristics")

        class ChecklistItem:
            tag = None
            value = None
            units = None

            def __init__(self, tag, characteristic):
                self.tag = tag
                self.value = characteristic.get("text")
                self.units = characteristic.get("unit")

        return [
            ChecklistItem(k, v[0]) for k, v in characteristics.items() if len(v) > 0
        ]

    def handle(self, *args, **options):
        animals_added = 0
        samples_added = 0

        for biosample in get_project_samples(
            options["project_attr"],
            options["webin_filter"],
            options["max_pages"],
            options["biosamples_page_cursor"],
            options["updated_since"],
        ):
            logging.info(f"Importing biosample {biosample.get('accession')}")

            if self.is_animal(biosample):
                system = self.get_system(biosample)
                if not system:
                    logging.warning(
                        f"Could not determine system for {biosample.get('accession')}"
                    )
                    continue
                animal, created = Animal.objects.get_or_create(
                    accession=biosample.get("accession"),
                    defaults={
                        "system": system,
                    },
                )
                structured_metadata = {
                    data_section.get("type"): data_section.get("content", [])
                    for data_section in biosample.get("structuredData", [])
                }

                animal.refresh_structureddata(
                    structured_metadata,
                )
                if created:
                    animals_added += 1
                    logging.info(f"Made animal {animal}")

            else:
                animal_accession = self.get_parent_animal(biosample)
                system = self.get_system(biosample)
                if not system:
                    logging.warning(
                        f"Could not determine system for {biosample.get('accession')}"
                    )
                    continue

                animal, created = Animal.objects.update_or_create(
                    accession=animal_accession,
                    defaults={
                        "system": system,
                    },
                )
                if created:
                    animals_added += 1
                    logging.info(
                        f"Made animal {animal} based on parentage of sample {biosample.get('accession')}"
                    )

                sample, created = Sample.objects.update_or_create(
                    accession=biosample.get("accession"),
                    defaults={
                        "animal": animal,
                        "title": self.get_from_characteristics(
                            biosample, "title", raise_if_none=False
                        )
                        or biosample.get("name", biosample.get("accession")),
                        "sample_type": self.get_sample_type(biosample),
                    },
                )
                structured_metadata = {
                    data_section.get("type"): data_section.get("content", [])
                    for data_section in biosample.get("structuredData", [])
                }

                sample.refresh_structureddata(
                    structured_metadata,
                    self.characteristics_to_checklist_obj(biosample),
                )
                sample.refresh_external_references(biosample.get("externalReferences"))
                if created:
                    samples_added += 1
                    logging.info(f"Made sample {sample}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Added {samples_added} samples and {animals_added} animals."
            )
        )
