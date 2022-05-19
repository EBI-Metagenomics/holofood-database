import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


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

    def setUp(self) -> None:
        super().setUp()

    def test_query(self):
        self.selenium.get(self.live_server_url + "/samples")
        wait = WebDriverWait(self.selenium, 10)

        project = self.hf_fixtures.projects[0]
        project_link = self.selenium.find_element(
            by=By.LINK_TEXT, value=project.accession
        )
        self.assertEqual(project_link.text, project.accession)
        assert "ena" in project_link.get_attribute("href")
