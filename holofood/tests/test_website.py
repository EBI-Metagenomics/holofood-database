import pytest
import requests_mock
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver

from selenium.webdriver.common.by import By

from holofood.models import ViralCatalogue, GenomeCatalogue
from holofood.tests.conftest import (
    salmon_metagenomics_analyses_response,
    mgnify_contig_response,
    mgnify_contig_annotations_response,
)
from holofood.utils import holofood_config


@pytest.mark.django_db
@pytest.mark.usefixtures("LiveTests")
class WebsiteTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.scopes = [
            ".*metagenomics/api.*",
            ".*viral-sequence-gff.*",
        ]  # URL patterns to intercept
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @requests_mock.Mocker()
    def test_web(self, m):
        # TODO: all test must be in one method currently... else fixtures dont work right

        wait = WebDriverWait(self.selenium, 10)

        # # ---- Home page ---- #
        self.selenium.get(self.live_server_url)
        self.selenium.add_cookie(
            {
                "name": "embl-ebi-public-website-v1.0-data-protection-accepted",
                "value": "true",
            }
        )

        samples_link = self.selenium.find_element(
            by=By.LINK_TEXT, value="Browse samples"
        )
        assert "/samples" in samples_link.get_attribute("href")

        # ---- Sample listing page ---- #
        self.selenium.get(self.live_server_url + "/samples")

        project = self.hf_fixtures.projects[0]
        project_link = self.selenium.find_element(
            by=By.LINK_TEXT, value=project.accession
        )
        self.assertEqual(project_link.text, project.accession)
        assert "ena" in project_link.get_attribute("href")

        # ---- Sample detail page ---- #
        project = self.hf_fixtures.projects[0]
        sample = self.hf_fixtures.samples[0]
        m.get(
            holofood_config.mgnify.api_root + f"/runs/ERR4918394/analyses",
            json=salmon_metagenomics_analyses_response(sample),
        )
        self.selenium.get(self.live_server_url + "/sample/" + sample.accession)
        project_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value=project.accession
        )
        self.assertIn(project.title, project_link.text)

        system_link = self.selenium.find_element(by=By.LINK_TEXT, value=sample.system)
        self.assertIn("salmon", system_link.get_attribute("href"))

        # # todo metadata table test
        metagenomics_expander_link = self.selenium.find_elements(
            by=By.TAG_NAME, value="summary"
        )[2]
        self.assertEqual(metagenomics_expander_link.text, "Metagenomics")
        metagenomics_expander_link.click()

        mgnify_link = self.selenium.find_element(
            by=By.LINK_TEXT, value="View sample on MGnify"
        )
        self.assertEqual(
            mgnify_link.get_attribute("href"),
            f"https://www.ebi.ac.uk/metagenomics/samples/{sample.accession}",
        )

        self.selenium.get(self.live_server_url + "/api/docs")
        list_link = self.selenium.find_element(by=By.LINK_TEXT, value="/api/samples")
        list_link.click()
        body = self.selenium.find_element(by=By.TAG_NAME, value="body")
        assert "HoloFood Data Portal API" in body.text

        # ---- MAG Catalogues ---- #
        catalogue: GenomeCatalogue = self.hf_fixtures.genome_catalogues[0]
        #  redirect to first catalogue should work
        self.selenium.get(self.live_server_url + "/genome-catalogues")
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url + "/genome-catalogue/" + catalogue.id,
        )

        export_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="Download all as TSV"
        )
        self.assertIn("export", export_link.get_attribute("href"))

        mgnify_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="Browse related catalogue"
        )
        self.assertIn(
            "metagenomics/genome-catalogues", mgnify_link.get_attribute("href")
        )

        species_rep_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="MGYG"
        )
        self.assertEqual(
            species_rep_link.text, catalogue.genomes.first().cluster_representative
        )

        # ---- Viral catalogues ---- #
        catalogue: ViralCatalogue = self.hf_fixtures.viral_catalogues[0]

        contig_requests = {
            holofood_config.mgnify.api_root
            + f"/analyses/{frag.mgnify_analysis_accession}/contigs/{frag.contig_id}": frag
            for frag in catalogue.viral_fragments.all()
        }
        annotation_requests = {
            holofood_config.mgnify.api_root
            + f"/analyses/{frag.mgnify_analysis_accession}/contigs/{frag.contig_id}/annotations": frag
            for frag in catalogue.viral_fragments.all()
        }

        # GFF should be available
        self.selenium.get(
            self.live_server_url
            + f"/viral-sequence-gff/{catalogue.viral_fragments.first().id}"
        )

        def interceptor(request):
            if request.url in contig_requests:
                request.create_response(
                    status_code=200,
                    headers={
                        "Content-Type": "text/x-fasta",
                        "Access-Control-Allow-Origin": "*",
                    },
                    body=mgnify_contig_response(contig_requests[request.url]),
                )
            if request.url in annotation_requests:
                request.create_response(
                    status_code=200,
                    headers={
                        "Content-Type": "text/x-gff3",
                        "Access-Control-Allow-Origin": "*",
                    },
                    body=mgnify_contig_annotations_response(
                        annotation_requests[request.url]
                    ),
                )
            if "viral-sequence-gff" in request.url:
                request.create_response(
                    status_code=200,
                    headers={
                        "Content-Type": "text/x-gff3",
                    },
                    # need to mock the GFF, for some reason IGV cannot load it by URL in unit tests...
                    body="MGYC001\tViPhOg\tCDS\t1020\t1990\t.\t-\t.\tID=MGYC001;viphog=ViPhOG1\n",
                )

        self.selenium.request_interceptor = interceptor

        #  redirect to first viral catalogue should work
        self.selenium.get(self.live_server_url + "/viral-catalogues")
        self.assertEqual(
            self.selenium.current_url,
            self.live_server_url + "/viral-catalogue/" + catalogue.id,
        )

        export_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="Download all as TSV"
        )
        self.assertIn("export", export_link.get_attribute("href"))

        mag_cat_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="Browse related MAG catalogue"
        )
        self.assertIn(
            catalogue.related_genome_catalogue.id, mag_cat_link.get_attribute("href")
        )

        parent_contig_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value=catalogue.viral_fragments.first().contig_id
        )
        self.assertIn("?selected_contig=", parent_contig_link.get_attribute("href"))

        view_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="View contig"
        )
        view_link.click()
        self.assertEqual(
            self.selenium.current_url,
            f"{self.live_server_url}/viral-catalogue/{catalogue.id}/{catalogue.viral_fragments.first().id}?",
        )
        gff_download_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="Download ViPhOGs GFF"
        )
        self.assertIn("viral-sequence-gff", gff_download_link.get_attribute("href"))

        wait.until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, "igv-contig-browser"), "Functional annotations"
            )
        )
        wait.until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, "igv-contig-browser"), "ViPhOGs"
            )
        )

        table = self.selenium.find_element(by=By.TAG_NAME, value="tbody")
        self.assertEqual(len(table.find_elements(by=By.TAG_NAME, value="tr")), 2)
        # One row for the species rep, one row for the link to the cluster

        cluster_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value="View cluster"
        )
        cluster_link.click()

        table = self.selenium.find_element(by=By.TAG_NAME, value="tbody")
        self.assertEqual(len(table.find_elements(by=By.TAG_NAME, value="tr")), 3)
        # One row for the species rep, one row for the link to cluster, one additional row for the cluster member

        del self.selenium.request_interceptor
