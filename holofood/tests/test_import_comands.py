import logging
import os.path
from io import StringIO


import pytest
from django.core.management import call_command


from holofood.external_apis.biosamples.api import API_ROOT as BSAPIROOT
from holofood.models import (
    Sample,
    ViralCatalogue,
    GenomeCatalogue,
    Animal,
    GenomeSampleContainment,
    Genome,
)
from holofood.utils import holofood_config

MGAPIROOT = holofood_config.mgnify.api_root.rstrip("/")


def _call_command(command, *args, **kwargs):
    out = StringIO()
    call_command(
        command,
        *args,
        stdout=out,
        stderr=StringIO(),
        **kwargs,
    )
    return out.getvalue()


@pytest.mark.django_db
def test_fetch_project_samples(requests_mock):
    requests_mock.get(
        f"{BSAPIROOT}/samples?filter=attr:project:HoloFood&size=200",
        json={
            "_links": {"next": {"href": None}},  # single page
            "_embedded": {
                "samples": [
                    {
                        "accession": "SAMEA1",
                        "name": "HF_DONUT.JAM.1",
                        "webinSubmissionAccountId": "Webin-good",  # project submitter
                        "relationships": [
                            {
                                "source": "SAMEA1",
                                "target": "SAMEG1",
                                "type": "DERIVED_FROM",
                            }
                        ],
                        "characteristics": {
                            "Organism": [{"text": "Salmo salar"}],
                            "project": [{"text": "HoloFood"}],
                        },
                        "structuredData": [
                            {
                                "type": "SAMPLE",
                                "content": [
                                    {
                                        "marker": {"value": "Experiment", "iri": None},
                                        "measurement": {
                                            "value": "histology",
                                            "iri": None,
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "accession": "SAMEA2",
                        "name": "HF_DONUT.EVIL.1",
                        "webinSubmissionAccountId": "Webin-bad",  # non-project submitter
                        "relationships": [
                            {
                                "source": "SAMEA2",
                                "target": "SAMEG1",
                                "type": "DERIVED_FROM",
                            }
                        ],
                        "characteristics": {
                            "Organism": [{"text": "Salmo salar"}],
                            "project": [{"text": "HoloFood"}],
                        },
                        "structuredData": [
                            {
                                "type": "SAMPLE",
                                "content": [
                                    {
                                        "marker": {"value": "Experiment", "iri": None},
                                        "measurement": {"value": "tm", "iri": None},
                                    }
                                ],
                            }
                        ],
                    },
                ]
            },
        },
    )
    requests_mock.get(
        f"{BSAPIROOT}/samples/SAMEA1",
        json={"externalReferences": [{"url": "fake://fakebiosamples/MTBLSDONUT"}]},
    )
    out = _call_command("fetch_project_samples", webin_filter=["Webin-good"])
    logging.info(out)
    assert Sample.objects.count() == 1
    # Sample from non-project webin is filtered out

    sample = Sample.objects.first()
    assert sample.title == "HF_DONUT.JAM.1"
    assert sample.sample_type == Sample.HISTOLOGICAL
    # should have set MTBLS ID from externalReferences call
    # (illogical in reality, but test case)
    assert sample.metabolights_study == "MTBLSDONUT"

    assert Animal.objects.count() == 1
    assert Animal.objects.first().accession == "SAMEG1"


@pytest.mark.django_db
def test_import_viral_catalogue(chicken_mag_catalogue):
    tests_path = os.path.dirname(__file__)
    out = _call_command(
        "import_viral_catalogue",
        "hf-donut-vir-cat-1",
        f"{tests_path}/static_fixtures/viral_catalogue/viral_cat.tsv",
        f"{tests_path}/static_fixtures/viral_catalogue/viral_cat.gff",
        title="Donut Viral Catalogue",
        related_mag_catalogue_id=chicken_mag_catalogue.id,
    )
    logging.info(out)

    assert ViralCatalogue.objects.filter(id="hf-donut-vir-cat-1").exists()

    created_catalogue = ViralCatalogue.objects.get(id="hf-donut-vir-cat-1")
    assert created_catalogue.title == "Donut Viral Catalogue"
    assert created_catalogue.biome == chicken_mag_catalogue.biome
    assert created_catalogue.system == chicken_mag_catalogue.system
    assert created_catalogue.viral_fragments.count() == 2

    fragment = created_catalogue.viral_fragments.get(id="MGYC003-start-512-end-768")
    assert fragment.cluster_representative.id == "MGYC001-start-256-end-512"
    assert "ViPhOG2" in fragment.gff
    assert fragment.start_within_contig == 512
    assert fragment.end_within_contig == 768


@pytest.mark.django_db
def test_import_mag_catalogue():
    tests_path = os.path.dirname(__file__)
    out = _call_command(
        "import_mag_catalogue",
        "hf-donut-mag-cat-1",
        f"{tests_path}/static_fixtures/mag-catalogue.tsv",
        "Donut MAG Catalogue",
        "public-donut-v1-0",
        "Donut Surface",
        "chicken",
    )
    logging.info(out)

    assert GenomeCatalogue.objects.filter(id="hf-donut-mag-cat-1").exists()

    created_catalogue = GenomeCatalogue.objects.get(id="hf-donut-mag-cat-1")
    assert created_catalogue.title == "Donut MAG Catalogue"
    assert created_catalogue.biome == "Donut Surface"
    assert created_catalogue.system == "chicken"
    assert created_catalogue.related_mag_catalogue_id == "public-donut-v1-0"
    assert created_catalogue.genomes.count() == 11
    assert (
        created_catalogue.genomes.order_by("-accession").first().taxonomy
        == "Bacteria > Firmicutes_A > Clostridia > Oscillospirales > Acutalibacteraceae > RUG420 > RUG420 sp900317985"
    )


@pytest.mark.django_db
def test_import_mag_sample_mapping(chicken_mag_catalogue, chicken_metagenomic_sample):
    tests_path = os.path.dirname(__file__)
    out = _call_command(
        "import_mag_sample_mapping",
        f"{tests_path}/static_fixtures/mag-sample-mapping.tsv",
        f"--catalogue_id_to_preclear={chicken_mag_catalogue.id}",
    )
    logging.info(out)

    assert GenomeSampleContainment.objects.count() == 1
    mag = Genome.objects.first()
    assert mag.samples_containing.count() == 1

    containment = GenomeSampleContainment.objects.first()
    assert containment.sample.accession == chicken_metagenomic_sample.accession
    assert containment.containment == 0.93
