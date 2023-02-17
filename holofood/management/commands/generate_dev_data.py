import logging
from typing import Union

from django.core.management.base import BaseCommand, CommandError

from holofood.models import Animal, Sample, SampleMetadataMarker


def _attach_metadata_to(
    marker_name: str,
    marker_type: str,
    sample: Union[Sample, Animal],
    measurement=None,
    units: str = None,
):
    marker, _ = SampleMetadataMarker.objects.get_or_create(
        name=marker_name,
        defaults={"iri": f"http://example.com/{marker_name}", "type": marker_type},
    )
    sample.structured_metadata.create(
        marker=marker, measurement=measurement, units=units
    )


METAB_FILES = [
    {
        "file_name": "ADG10003u_007.zip",
        "reliability": "1.0",
        "sample_name": "ADG10003u_007",
    },
    {
        "file_name": "ADG10003u_007.nmrML",
        "reliability": "1.0",
        "sample_name": "ADG10003u_007",
    },
]


class Command(BaseCommand):
    help = "Fills the database with a few pieces of data for development purposes."

    def handle(self, *args, **options):
        charlie_chicken = Animal.objects.create(
            accession="SAMEG01",
            system=Animal.CHICKEN,
            animal_code="CCHARLIE",
        )
        chantelle_chicken = Animal.objects.create(
            accession="SAMEG02",
            system=Animal.CHICKEN,
            animal_code="CCHANTELLE",
        )
        sandy_salmon = Animal.objects.create(
            accession="SAMEG03",
            system=Animal.SALMON,
            animal_code="SSANDY",
        )
        sophie_salmon = Animal.objects.create(
            accession="SAMEG04",
            system=Animal.SALMON,
            animal_code="SSOPHIE",
        )
        charlie_metagen = Sample.objects.create(
            accession="SAMEA01",
            animal=charlie_chicken,
            sample_type=Sample.METAGENOMIC,
            title="chicken caecum extraction",
            ena_run_accessions=["ERR4918394"],
        )
        chantelle_metagen = Sample.objects.create(
            accession="SAMEA02",
            animal=chantelle_chicken,
            sample_type=Sample.METAGENOMIC,
            title="chicken ileum extraction",
            ena_run_accessions=["ERR4918394"],
        )
        charlie_metab = Sample.objects.create(
            accession="SAMEA03",
            animal=charlie_chicken,
            sample_type=Sample.METABOLOMIC,
            title="chicken untargeted metabolomics",
            metabolights_files=METAB_FILES,
        )
        charlie_hist = Sample.objects.create(
            accession="SAMEA04",
            animal=charlie_chicken,
            sample_type=Sample.HISTOLOGICAL,
            title="chicken histological",
        )
        charlie_host = Sample.objects.create(
            accession="SAMEA05",
            animal=charlie_chicken,
            sample_type=Sample.HOST_GENOMIC,
            title="chicken host genome",
        )
        sandy_host = Sample.objects.create(
            accession="SAMEA06",
            animal=sandy_salmon,
            sample_type=Sample.HOST_GENOMIC,
            title="salmon host genome",
        )
        sandy_metag = Sample.objects.create(
            accession="SAMEA07",
            animal=sandy_salmon,
            sample_type=Sample.METAGENOMIC,
            title="salmon extraction",
            ena_run_accessions=["ERR4918394"],
        )
        sophie_metag = Sample.objects.create(
            accession="SAMEA08",
            animal=sophie_salmon,
            sample_type=Sample.METAGENOMIC,
            title="salmon extraction",
            ena_run_accessions=["ERR4918394"],
        )
        sophie_metab = Sample.objects.create(
            accession="SAMEA09",
            animal=sophie_salmon,
            sample_type=Sample.METABOLOMIC,
            title="salmon extraction",
            metabolights_files=METAB_FILES,
        )
        sophie_hist = Sample.objects.create(
            accession="SAMEA10",
            animal=sophie_salmon,
            sample_type=Sample.HISTOLOGICAL,
            title="salmon extraction",
        )

        animal_metadata = {
            "host diet treatment concentration": ([0.1, 0.2, 0.15, 0.21], "%"),
            "host diet treatment": (
                ["Control", "Cornflakes", "Control", "Seaweed"],
                None,
            ),
            "trial timepoint": ([30, 60, 21, 42], "days"),
            "host length": ([50, 60, 20, 30], "cm"),
        }

        for marker_name, data in animal_metadata.items():
            units = data[1]
            for animal, measurement in zip(
                [charlie_chicken, chantelle_chicken, sandy_salmon, sophie_salmon],
                data[0],
            ):
                _attach_metadata_to(
                    marker_name,
                    "ANIMAL_LEVEL_BIOSAMPLES_METADATA",
                    animal,
                    measurement,
                    units,
                )

        _attach_metadata_to("average end weight", "TANK", sandy_salmon, 500, "g")
        _attach_metadata_to("average end weight", "TANK", sophie_salmon, 600, "g")
        _attach_metadata_to(
            "average body weight at day 21", "PEN", charlie_chicken, 1000, "g"
        )
        _attach_metadata_to(
            "average body weight at day 21", "PEN", chantelle_chicken, 1200, "g"
        )

        _attach_metadata_to("histology marker 1", "HISTOLOGY", charlie_hist, 0.1, "um")
        _attach_metadata_to("histology marker 2", "HISTOLOGY", charlie_hist, 0.7, "um")
        _attach_metadata_to("histology marker 1", "HISTOLOGY", sophie_hist, 0.3, "um")

        for a in range(5, 20):
            animal = Animal.objects.create(
                accession=f"SAMEG{a:02d}",
                system=Animal.CHICKEN,
                animal_code=f"EXTRACHI{a}",
            )
            for marker_name in animal_metadata.keys():
                _attach_metadata_to(marker_name, None, animal, 0)

            for s in range(5):
                Sample.objects.create(
                    animal=animal,
                    title=f"extra chicken sample {a}-{s}",
                    accession=f"SAMEA{a*10 + s}",
                    sample_type=Sample.METAGENOMIC,
                )

        for a in range(30, 50):
            animal = Animal.objects.create(
                accession=f"SAMEG{a:02d}",
                system=Animal.SALMON,
                animal_code=f"EXTRASAL{a}",
            )
            for marker_name in animal_metadata.keys():
                _attach_metadata_to(marker_name, None, animal, 0)
            for s in range(5):
                Sample.objects.create(
                    animal=animal,
                    title=f"extra salmon sample {a}-{s}",
                    accession=f"SAMEA{a * 10 + s}",
                    sample_type=Sample.METAGENOMIC,
                )
