from typing import Union

from django.core.management.base import BaseCommand, CommandError

from holofood.models import (
    Animal,
    Sample,
    SampleMetadataMarker,
    AnalysisSummary,
    GenomeCatalogue,
    Genome,
    ViralCatalogue,
    ViralFragment,
)


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


class Command(BaseCommand):
    help = "Fills the database with a few pieces of data for development purposes."

    def handle(self, *args, **options):
        Animal.objects.all().delete()
        AnalysisSummary.objects.all().delete()
        GenomeCatalogue.objects.all().delete()
        ViralCatalogue.objects.all().delete()

        charlie_chicken = Animal.objects.create(
            accession="SAMEG01",
            system=Animal.CHICKEN,
        )
        chantelle_chicken = Animal.objects.create(
            accession="SAMEG02",
            system=Animal.CHICKEN,
        )
        sandy_salmon = Animal.objects.create(
            accession="SAMEG03",
            system=Animal.SALMON,
        )
        sophie_salmon = Animal.objects.create(
            accession="SAMEG04",
            system=Animal.SALMON,
        )
        charlie_metagen = Sample.objects.create(
            accession="SAMEA01",
            animal=charlie_chicken,
            sample_type=Sample.METAGENOMIC_ASSEMBLY,
            title="chicken caecum extraction",
        )
        chantelle_metagen = Sample.objects.create(
            accession="SAMEA02",
            animal=chantelle_chicken,
            sample_type=Sample.METAGENOMIC_ASSEMBLY,
            title="chicken ileum extraction",
        )
        charlie_metab = Sample.objects.create(
            accession="SAMEA03",
            animal=charlie_chicken,
            sample_type=Sample.METABOLOMIC,
            title="chicken untargeted metabolomics",
            metabolights_study="MTBLS1",
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
            sample_type=Sample.METAGENOMIC_ASSEMBLY,
            title="salmon extraction",
        )
        sophie_metag = Sample.objects.create(
            accession="SAMEA08",
            animal=sophie_salmon,
            sample_type=Sample.METAGENOMIC_ASSEMBLY,
            title="salmon extraction",
        )
        sophie_metab = Sample.objects.create(
            accession="SAMEA09",
            animal=sophie_salmon,
            sample_type=Sample.METABOLOMIC,
            title="salmon extraction",
            metabolights_study="MTBLS1",
        )
        sophie_hist = Sample.objects.create(
            accession="SAMEA10",
            animal=sophie_salmon,
            sample_type=Sample.HISTOLOGICAL,
            title="salmon extraction",
        )

        animal_metadata = {
            "Treatment concentration": ([0.1, 0.2, 0.15, 0.21], "%"),
            "Treatment name": (
                ["Control", "Cornflakes", "Control", "Seaweed"],
                None,
            ),
            "Sampling time": ([30, 60, 21, 42], "days"),
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

        _attach_metadata_to(
            "Metabolights accession", "METABOLIGHTS", charlie_metab, "MTBLS1", ""
        )
        _attach_metadata_to(
            "Metabolights accession", "METABOLIGHTS", sophie_metab, "MTBLS2", ""
        )

        for a in range(5, 20):
            animal = Animal.objects.create(
                accession=f"SAMEG{a:02d}",
                system=Animal.CHICKEN,
            )
            for marker_name in animal_metadata.keys():
                _attach_metadata_to(marker_name, None, animal, 0)

            for s in range(5):
                Sample.objects.create(
                    animal=animal,
                    title=f"extra chicken sample {a}-{s}",
                    accession=f"SAMEA{a*10 + s}",
                    sample_type=Sample.METAGENOMIC_ASSEMBLY,
                )

        for a in range(30, 50):
            animal = Animal.objects.create(
                accession=f"SAMEG{a:02d}",
                system=Animal.SALMON,
            )
            for marker_name in animal_metadata.keys():
                _attach_metadata_to(marker_name, None, animal, 0)
            for s in range(5):
                Sample.objects.create(
                    animal=animal,
                    title=f"extra salmon sample {a}-{s}",
                    accession=f"SAMEA{a * 10 + s}",
                    sample_type=Sample.METAGENOMIC_ASSEMBLY,
                )

        summary = AnalysisSummary.objects.create(
            slug="fish-viruses",
            title="Salmon viral catalogue info",
            content="""## Viral fragments found
Fish in Trial A...
![Viral fragments found](https://www.holofood.eu/files/salmon.png)""",
            is_published=True,
            author="HoloFood Team",
        )
        summary.samples.add(sophie_metag)

        genome_catalogue = GenomeCatalogue.objects.create(
            id="hf-mag-cat-v1",
            title="HoloFood Salmon MAG Catalogue v1.0",
            biome="Salmon Gut",
            related_mag_catalogue_id="non-model-fish-gut-v1-0",
            system=Animal.SALMON,
        )

        Genome.objects.create(
            accession="MGYG000299500",
            cluster_representative="MGYG000299502",
            catalogue=genome_catalogue,
            taxonomy="Bacteria > Proteobacteria > Gammaproteobacteria > Enterobacterales > Enterobacteriaceae > Escherichia > Escherichia coli",
            metadata={},
        )

        summary.genome_catalogues.add(genome_catalogue)

        viral_catalogue = ViralCatalogue.objects.create(
            id="hf-salmon-vir-cat-v1",
            title="HoloFood Salmon Viral Catalogue v1",
            biome="Salmon Gut",
            related_genome_catalogue=genome_catalogue,
            system=Animal.SALMON,
        )
        rep = ViralFragment.objects.create(
            id="MGYC001-start-1000-end-2000",
            catalogue=viral_catalogue,
            start_within_contig=1000,
            end_within_contig=2000,
            contig_id="ERZ2627283.1-NODE-1-length-143081-cov-101.301728",
            viral_type=ViralFragment.PROPHAGE,
            mgnify_analysis_accession="MGYA00606123",
            gff="ERZ2627283.1-NODE-1-length-143081-cov-101.301728\tViPhOg\tCDS\t1020\t1990\t.\t-\t.\tID=MGYC001;viphog=ViPhOG1\n",
        )
        ViralFragment.objects.create(
            id="MGYC001-start-3000-end-4000",
            catalogue=viral_catalogue,
            start_within_contig=3000,
            end_within_contig=4000,
            contig_id="ERZ2627283.1-NODE-1-length-143081-cov-101.301728",
            viral_type=ViralFragment.PROPHAGE,
            mgnify_analysis_accession="MGYA00606123",
            cluster_representative=rep,
            gff="ERZ2627283.1-NODE-1-length-143081-cov-101.301728\tViPhOg\tCDS\t3020\t3090\t.\t-\t.\tID=MGYC001;viphog=ViPhOG2\n",
        )

        summary.viral_catalogues.add(viral_catalogue)
