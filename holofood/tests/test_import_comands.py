import logging
from io import StringIO


import pytest
from django.core.management import call_command


from holofood.external_apis.ena.portal_api import API_ROOT as ENAAPIROOT
from holofood.external_apis.biosamples.api import API_ROOT as BSAPIROOT
from holofood.external_apis.ena.submit_api import API_ROOT as DBAPIROOT
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
def test_refresh_structureddata(
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
    out = _call_command("refresh_structureddata", sample=salmon_sample.accession)
    logging.info(out)
    assert (
        salmon_sample.structured_metadata.count() == 51
    )  # 51 = SAMPLE-type markers from structureddata + ENA checklist

    # self.assertEqual(out, "In dry run mode (--write not passed)\n")

    # book_empty.refresh_from_db()
    # self.assertEqual(book_empty.title, "")

    # def test_write_empty(self):
    #     book_empty = Book.objects.create(title="")
    #
    #     out = self.call_command("--write")
    #
    #     self.assertEqual(out, "Updated 1 book(s)\n")
    #     book_empty.refresh_from_db()
    #     self.assertEqual(book_empty.title, "Unknown")
    #
    # def test_write_lowercase(self):
    #     book_lowercase = Book.objects.create(title="lowercase")
    #
    #     out = self.call_command("--write")
    #
    #     self.assertEqual(out, "Updated 1 book(s)\n")
    #     book_lowercase.refresh_from_db()
    #     self.assertEqual(book_lowercase.title, "Lowercase")
    #
    # def test_write_full_stop(self):
    #     book_full_stop = Book.objects.create(title="Full Stop.")
    #
    #     out = self.call_command("--write")
    #
    #     self.assertEqual(out, "Updated 1 book(s)\n")
    #     book_full_stop.refresh_from_db()
    #     self.assertEqual(book_full_stop.title, "Full Stop")
    #
    # def test_write_ampersand(self):
    #     book_ampersand = Book.objects.create(title="Dombey & Son")
    #
    #     out = self.call_command("--write")
    #
    #     self.assertEqual(out, "Updated 1 book(s)\n")
    #     book_ampersand.refresh_from_db()
    #     self.assertEqual(book_ampersand.title, "Dombey and Son")
