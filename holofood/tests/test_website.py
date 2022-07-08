import pytest
import requests_mock
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from holofood.tests.conftest import salmon_metagenomics_analyses_response
from holofood.utils import holofood_config


@pytest.mark.django_db
@pytest.mark.usefixtures("LiveTests")
class WebsiteTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @requests_mock.Mocker()
    def test_web(self, m):
        # TODO: all test must be in one method currently... else fixtures dont work right

        # ---- Home page ---- #
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
        catalogue = self.hf_fixtures.genome_catalogues[0]
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
