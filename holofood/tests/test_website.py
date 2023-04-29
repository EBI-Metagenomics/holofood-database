import time

import pytest
import requests_mock
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver

from selenium.webdriver.common.by import By

from holofood.models import ViralCatalogue, GenomeCatalogue
from holofood.tests.conftest import (
    salmon_metagenomics_analyses_response,
    mgnify_contig_response,
    mgnify_contig_annotations_response,
    metabolights_study_file_response,
    metabolights_study_sheet_response,
    metabolights_assay_sheet_response,
    ena_sample_file_report_response,
)
from holofood.utils import holofood_config


@pytest.mark.django_db
@pytest.mark.usefixtures("LiveTests")
class WebsiteTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
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
        # All tests must be in one method currently... else fixtures don't work right

        wait = WebDriverWait(self.selenium, 10)

        # # ---- Home page ---- #
        self.selenium.get(self.live_server_url)
        self.selenium.add_cookie(
            {
                "name": "emblContentHub27360_224467",
                "value": "true",
            }
        )

        samples_link = self.selenium.find_element(
            by=By.LINK_TEXT, value="Browse samples"
        )
        assert "/samples" in samples_link.get_attribute("href")

        # ---- Sample listing page ---- #
        self.selenium.get(self.live_server_url + "/samples")

        animal = self.hf_fixtures.animals[0]
        animal_link = self.selenium.find_element(
            by=By.LINK_TEXT, value=animal.accession
        )
        self.assertEqual(animal_link.text, animal.accession)
        assert "animal" in animal_link.get_attribute("href")

        # Samples list for specific animal
        self.selenium.get(
            f"{self.live_server_url}/samples/?animal_accession__icontains={animal.accession}"
        )
        breadcrumbs = self.selenium.find_element(
            by=By.CLASS_NAME, value="vf-breadcrumbs"
        )
        assert f"Animal {animal.accession}" in breadcrumbs.text

        # Sample list filter
        system_filter = Select(
            self.selenium.find_element(
                by=By.XPATH, value="//select[@name='animal__system']"
            )
        )
        system_filter.select_by_visible_text("salmon")
        apply_button = self.selenium.find_element(
            by=By.XPATH, value="//*[@id='sample_filters']//input[@type='submit']"
        )
        apply_button.click()

        system_filter = Select(
            self.selenium.find_element(
                by=By.XPATH, value="//select[@name='animal__system']"
            )
        )
        self.assertEqual(system_filter.first_selected_option.text, "salmon")
        table_rows = self.selenium.find_elements(
            by=By.CLASS_NAME, value="vf-table__row"
        )
        self.assertEqual(len(table_rows), 4)  # header, 2 samples, footer

        system_filter.select_by_visible_text("chicken")
        apply_button = self.selenium.find_element(
            by=By.XPATH, value="//*[@id='sample_filters']//input[@type='submit']"
        )
        apply_button.click()

        table_rows = self.selenium.find_elements(
            by=By.CLASS_NAME, value="vf-table__row"
        )
        self.assertEqual(len(table_rows), 2)  # header, footer

        # treatment search
        self.selenium.get(f"{self.live_server_url}/samples/?metadata_search=cornfl")
        table_rows = self.selenium.find_elements(
            by=By.CLASS_NAME, value="vf-table__row"
        )
        self.assertEqual(len(table_rows), 4)  # header, footer, 2 samples from animal 1
        cornflakes_cells = self.selenium.find_elements(
            by=By.XPATH, value="//td[text()='Cornflakes']"
        )
        self.assertEqual(len(cornflakes_cells), 2)

        self.selenium.get(f"{self.live_server_url}/samples/?metadata_search=ice cream")
        table_rows = self.selenium.find_elements(
            by=By.CLASS_NAME, value="vf-table__row"
        )
        self.assertEqual(len(table_rows), 2)  # header, footer, 0 samples

        # ---- Sample detail page ---- #
        sample = self.hf_fixtures.samples[0]
        m.get(
            holofood_config.metabolights.api_root
            + f"/studies/MTBLSDONUT/files?include_raw_data=false",
            json=metabolights_study_file_response(),
        )
        m.get(
            holofood_config.metabolights.api_root
            + f"/studies/MTBLSDONUT/download?file=s_mtbls.txt",
            body=metabolights_study_sheet_response(sample),
        )
        m.get(
            holofood_config.metabolights.api_root
            + f"/studies/MTBLSDONUT/download?file=a_assay.txt",
            body=metabolights_assay_sheet_response(),
        )
        self.selenium.get(self.live_server_url + "/sample/" + sample.accession)
        animal_link = self.selenium.find_element(
            by=By.PARTIAL_LINK_TEXT, value=animal.accession
        )
        self.assertIn(animal.accession, animal_link.text)

        type_link = self.selenium.find_element(by=By.LINK_TEXT, value="metabolomic")
        self.assertIn("metabolomic", type_link.get_attribute("href"))

        metabolomics_expander_link = self.selenium.find_elements(
            by=By.TAG_NAME, value="summary"
        )[2]
        self.assertEqual(metabolomics_expander_link.text, "Metabolomics")
        metabolomics_expander_link.click()

        metabolights_link = self.selenium.find_element(
            by=By.LINK_TEXT, value="View project MTBLSDONUT on MetaboLights"
        )
        self.assertEqual(
            metabolights_link.get_attribute("href"),
            f"https://www.ebi.ac.uk/metabolights/MTBLSDONUT",
        )

        download_link = self.selenium.find_element(by=By.LINK_TEXT, value="raw.sheet")
        self.assertEqual(
            download_link.get_attribute("href"),
            "https://www.ebi.ac.uk/metabolights/ws/studies/MTBLSDONUT/download/public?file=raw.sheet",
        )

        # METAGENOMICS
        sample = self.hf_fixtures.samples[1]
        m.get(
            holofood_config.mgnify.api_root
            + f"/analyses?sample_accession={sample.accession}",
            json=salmon_metagenomics_analyses_response(sample),
        )
        m.get(
            holofood_config.ena.portal_api_root
            + f"/filereport?result=read_run&accession={sample.accession}&format=json",
            json=ena_sample_file_report_response(sample),
        )
        self.selenium.get(self.live_server_url + "/sample/" + sample.accession)

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

        sequencing_expander_link = self.selenium.find_elements(
            by=By.TAG_NAME, value="summary"
        )[3]
        self.assertEqual(sequencing_expander_link.text, "Nucleotide sequencing data")
        sequencing_expander_link.click()

        ena_link = self.selenium.find_element(
            by=By.LINK_TEXT, value=f"View sample {sample.accession} in ENA"
        )
        self.assertEqual(
            ena_link.get_attribute("href"),
            f"https://www.ebi.ac.uk/ena/browser/view/{sample.accession}",
        )
        run_link = self.selenium.find_element(by=By.LINK_TEXT, value="ERR1")
        self.assertEqual(
            run_link.get_attribute("href"),
            "https://www.ebi.ac.uk/ena/browser/view/ERR1",
        )
        exp_link = self.selenium.find_element(by=By.LINK_TEXT, value="ERX1")
        self.assertEqual(
            exp_link.get_attribute("href"),
            "https://www.ebi.ac.uk/ena/browser/view/ERX1",
        )
        prj_link = self.selenium.find_element(by=By.LINK_TEXT, value="PRJ1")
        self.assertEqual(
            prj_link.get_attribute("href"),
            "https://www.ebi.ac.uk/ena/browser/view/PRJ1",
        )

        # METADATA TABLE
        metadata_expander_link = self.selenium.find_elements(
            by=By.TAG_NAME, value="summary"
        )[1]
        self.assertEqual(metadata_expander_link.text, "Sample metadata")
        metadata_expander_link.click()
        tabs = self.selenium.find_elements(
            by=By.XPATH, value="//ul[@id='metadata-sections-tabs']/li"
        )
        self.assertEqual(len(tabs), 2)

        dimensions_tab = self.selenium.find_element(by=By.LINK_TEXT, value="Dimensions")
        dimensions_tab.click()

        metadata_table = self.selenium.find_element(
            by=By.XPATH, value="//section[@id='vf-tabs__section--dimensions']"
        )
        self.assertIn("Size of donut", metadata_table.text)
        self.assertIn("10", metadata_table.text)
        self.assertIn("cm", metadata_table.text)

        metadata_search_box = self.selenium.find_element(
            by=By.XPATH, value="//input[@placeholder='Search metadata markers']"
        )

        metadata_search_box.send_keys("siz")
        matching_markers = self.selenium.find_elements(
            by=By.XPATH, value="//ul[@class='typeahead-results']/li"
        )
        self.assertEqual(len(matching_markers), 1)
        self.assertIn("Size of donut", matching_markers[0].text)
        metadata_search_box.clear()

        metadata_search_box.send_keys("colo")
        # wait for typeahead
        match = self.selenium.find_element(
            by=By.XPATH, value="//ul[@class='typeahead-results']/li"
        )
        metadata_search_box.send_keys(Keys.DOWN)
        colours_tab = self.selenium.find_element(
            by=By.XPATH, value="//a[@data-metadata-type-key='COLOURS']"
        )
        self.assertIn("highlight-tab-match", colours_tab.get_attribute("class"))
        match.click()

        metadata_table = self.selenium.find_element(
            by=By.XPATH, value="//section[@id='vf-tabs__section--colours']"
        )
        self.assertTrue(metadata_table.is_displayed())
        self.assertIn("Colour of donut", metadata_table.text)
        self.assertIn("Yellow", metadata_table.text)

        # ---- Animal listing page ---- #

        self.selenium.get(self.live_server_url + "/animals")

        animal = self.hf_fixtures.animals[0]
        animal_link = self.selenium.find_element(
            by=By.LINK_TEXT, value=animal.accession
        )
        self.assertEqual(animal_link.text, animal.accession)
        assert animal.accession in animal_link.get_attribute("href")

        samples_link = self.selenium.find_element(by=By.LINK_TEXT, value="2 samples")
        assert (
            f"animal_accession__icontains={animal.accession}"
            in samples_link.get_attribute("href")
        )

        # ---- Animal detail page ---- #
        self.selenium.get(self.live_server_url + "/animal/" + animal.accession)

        system_link = self.selenium.find_element(by=By.LINK_TEXT, value="salmon")
        assert "?system=salmon" in system_link.get_attribute("href")

        samples_link = self.selenium.find_element(
            by=By.LINK_TEXT, value="View 2 derived samples"
        )
        assert (
            f"animal_accession__icontains={animal.accession}"
            in samples_link.get_attribute("href")
        )

        # ---- API Docs ---- #
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

        # ---- Global Search ---- #
        animal = self.hf_fixtures.animals[0]
        sample = self.hf_fixtures.samples[0]

        m.get(
            f"{holofood_config.docs.docs_url}/search.json",
            json=[],
        )

        # Partial search should work
        def get_search_box():
            return self.selenium.find_element(
                by=By.XPATH, value="//input[@placeholder='Search data and docs']"
            )

        # get_search_box().send_keys(animal.animal_code.lower())
        # get_search_box().send_keys(Keys.ENTER)
        # self.assertEqual(
        #     self.selenium.current_url,
        #     f"{self.live_server_url}/search/?query={animal.animal_code.lower().replace(' ', '+')}",
        # )
        # self.assertIn(
        #     animal.accession,
        #     self.selenium.find_element(by=By.TAG_NAME, value="body").text,
        # )

        # Searching for exact sample accession should go straight to detail page
        get_search_box().send_keys(sample.accession)
        get_search_box().send_keys(Keys.ENTER)
        self.assertEqual(
            self.selenium.current_url,
            f"{self.live_server_url}/sample/{sample.accession}",
        )

        # Searching for exact animal accession should go straight to detail page
        get_search_box().send_keys(animal.accession)
        get_search_box().send_keys(Keys.ENTER)
        self.assertEqual(
            self.selenium.current_url,
            f"{self.live_server_url}/animal/{animal.accession}",
        )
