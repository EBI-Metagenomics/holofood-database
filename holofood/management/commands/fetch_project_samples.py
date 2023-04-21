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

    # @staticmethod
    # def _sample_for_run(run):
    #     return run["sample_accession"]

    @staticmethod
    def is_animal(sample: dict) -> bool:
        has_no_parent = len(sample.get("relationships", [])) == 0
        return has_no_parent

    @staticmethod
    def get_system(sample: dict) -> str:
        host_tax_id = Command.get_from_characteristics(sample, "host tax id")
        if not host_tax_id:
            # Some samples have this without whitespace...
            host_tax_id = Command.get_from_characteristics(sample, "host taxid")
        return holofood_config.ena.systems.get(host_tax_id)

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
        if experiment_type in ["metagenomic", "metagenomics"]:
            return Sample.METAGENOMIC
        else:
            # TODO: fix me
            return Sample.METABOLOMIC

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
        samples = get_project_samples(options["project_attr"], options["webin_filter"])
        animals_added = 0
        samples_added = 0

        for biosample in samples:
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
                        "animal_code": self.get_from_characteristics(
                            biosample, "title"
                        ),
                    },
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

                animal, created = Animal.objects.get_or_create(
                    accession=animal_accession,
                    defaults={
                        "system": system,
                        "animal_code": self.get_from_characteristics(
                            biosample, "host subject id"
                        ),
                    },
                )
                if created:
                    animals_added += 1
                    logging.info(
                        f"Made animal {animal} based on parentage of sample {biosample.get('accession')}"
                    )

                sample, created = Sample.objects.get_or_create(
                    accession=biosample.get("accession"),
                    defaults={
                        "animal": animal,
                        "title": self.get_from_characteristics(
                            biosample, "title", raise_if_none=True
                        ),
                        "sample_type": self.get_from_structured_data(
                            biosample, "SAMPLE", "Experiment"
                        ),
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
                if created:
                    samples_added += 1
                    logging.info(f"Made sample {sample}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Added {samples_added} samples and {animals_added} animals."
            )
        )
