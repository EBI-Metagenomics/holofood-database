import logging
from io import StringIO


import pytest
from django.core.management import call_command


from holofood.external_apis.ena.portal_api import API_ROOT as ENAAPIROOT
from holofood.external_apis.biosamples.api import API_ROOT as BSAPIROOT
from holofood.external_apis.ena.submit_api import API_ROOT as DBAPIROOT
from holofood.external_apis.mgnify.api import API_ROOT as MGAPIROOT
from holofood.models import Sample, Project


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
        f"{ENAAPIROOT}/search?format=json&dataPortal=metagenome&result=read_run&query=study_accession=PRJTESTING&fields=sample_accession,project_name,sample_title,checklist",
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
):
    requests_mock.get(
        f"{BSAPIROOT}/structureddata/{salmon_sample.accession}",
        json=salmon_structureddata_response,
    )
    requests_mock.get(
        f"{DBAPIROOT}/drop-box/samples/{salmon_sample.accession}",
        text=salmon_submitted_checklist,
    )
    out = _call_command(
        "refresh_external_data", samples=salmon_sample.accession, types=["METADATA"]
    )
    logging.info(out)
    assert (
        salmon_sample.structured_metadata.count() == 168
    )  # 168 =  markers from structureddata + ENA checklist

    requests_mock.get(
        f"{MGAPIROOT}/samples/{salmon_sample.accession}",
        status_code=404,  # 404 means sample not in MGnify
        text="anything",
    )
    out = _call_command(
        "refresh_external_data",
        samples=salmon_sample.accession,
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
        "refresh_external_data", samples=salmon_sample.accession, types=["METAGENOMIC"]
    )
    logging.info(out)
    salmon_sample.refresh_from_db()
    assert salmon_sample.has_metagenomics
