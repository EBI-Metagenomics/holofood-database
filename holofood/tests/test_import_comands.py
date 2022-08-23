import logging
import os.path
from io import StringIO


import pytest
from django.core.management import call_command


from holofood.external_apis.ena.portal_api import API_ROOT as ENAAPIROOT
from holofood.external_apis.biosamples.api import API_ROOT as BSAPIROOT
from holofood.external_apis.ena.browser_api import API_ROOT as DBAPIROOT
from holofood.external_apis.metabolights.api import API_ROOT as MTBLSAPIROOT
from holofood.models import Sample, Project, ViralCatalogue, GenomeCatalogue
from holofood.tests.conftest import set_metabolights_project_for_sample
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
        f"{ENAAPIROOT}/search?format=json&dataPortal=ena&result=read_run&query=study_accession=PRJTESTING&fields=sample_accession,project_name,sample_title,checklist",
        json=[
            {
                "run_accession": "ERR0000001",
                "sample_accession": "SAMEA00000001",
                "project_name": "HoloFood Donut",
                "sample_title": "HF_DONUT.JAM.1",
                "checklist": "ERC000052",
            },
        ],
    )
    out = _call_command("fetch_project_samples")
    logging.info(out)
    assert Project.objects.count() == 1
    assert Sample.objects.count() == 1

    sample = Sample.objects.first()
    assert sample.project.title == "HoloFood Donut"
    assert sample.title == "HF_DONUT.JAM.1"


@pytest.mark.django_db
def test_refresh_external_data(
    requests_mock,
    salmon_sample: Sample,
    salmon_structureddata_response,
    salmon_submitted_checklist,
    salmon_sample_metabolights_response,
):
    requests_mock.get(
        f"{BSAPIROOT}/structureddata/{salmon_sample.accession}",
        json=salmon_structureddata_response,
    )
    requests_mock.get(
        f"{DBAPIROOT}/xml/{salmon_sample.accession}",
        text=salmon_submitted_checklist,
    )
    out = _call_command(
        "refresh_external_data", samples=[salmon_sample.accession], types=["METADATA"]
    )
    logging.info(out)
    assert (
        salmon_sample.structured_metadata.count() == 182
    )  # 182 =  distincted (per section) markers from structureddata + ENA checklist

    requests_mock.get(
        f"{MGAPIROOT}/samples/{salmon_sample.accession}",
        status_code=404,  # 404 means sample not in MGnify
        text="anything",
    )
    out = _call_command(
        "refresh_external_data",
        samples=[salmon_sample.accession],
        types=["METADATA", "METAGENOMIC"],
    )
    logging.info(out)
    salmon_sample.refresh_from_db()
    assert not salmon_sample.has_metagenomics

    requests_mock.get(
        f"{MGAPIROOT}/samples/{salmon_sample.accession}",
        status_code=200,  # 200 means sample is in MGnify
        text="anything",
    )
    out = _call_command(
        "refresh_external_data",
        samples=[salmon_sample.accession],
        types=["METAGENOMIC"],
    )
    logging.info(out)
    salmon_sample.refresh_from_db()
    assert salmon_sample.has_metagenomics

    set_metabolights_project_for_sample(salmon_sample)
    salmon_sample.refresh_from_db()
    logging.warning(
        f"WILLBE{MTBLSAPIROOT}/studies/{salmon_sample.metabolights_project}/files/samples"
    )
    requests_mock.get(
        f"{MTBLSAPIROOT}/studies/{salmon_sample.metabolights_project}/files/samples",
        status_code=200,
        json=salmon_sample_metabolights_response,
    )
    out = _call_command(
        "refresh_external_data",
        samples=[salmon_sample.accession],
        types=["METABOLOMIC"],
    )
    logging.info(out)
    salmon_sample.refresh_from_db()
    assert salmon_sample.has_metabolomics
    assert len(salmon_sample.metabolights_files) == 2
    assert "donut" in salmon_sample.metabolights_files[0]["file_name"]


@pytest.mark.django_db
def test_import_viral_catalogue(chicken_mag_catalogue):
    tests_path = os.path.dirname(__file__)
    out = _call_command(
        "import_viral_catalogue",
        "hf-donut-vir-cat-1",
        f"{tests_path}/static_fixtures/viral_catalogue/viral_cat.tsv",
        f"{tests_path}/static_fixtures/viral_catalogue",
        "Donut Viral Catalogue",
        chicken_mag_catalogue.id,
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
