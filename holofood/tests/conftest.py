import pytest

from holofood.models import Project, Sample


@pytest.fixture
def salmon_project():
    return Project.objects.create(
        accession="PRJTESTING", title="HoloFood Donut and Fish"
    )


@pytest.fixture()
def salmon_sample(salmon_project):
    return Sample.objects.create(
        accession="SAMEA00000002",
        project=salmon_project,
        title="HF_DONUT.SALMON.1",
        system=Sample.SALMON,
    )


@pytest.fixture()
def salmon_structureddata_response(salmon_sample):
    return {
        "accession": salmon_sample.accession,
        "create": "2022-05-05T14:16:35.502Z",
        "update": "2022-05-05T14:16:35.506Z",
        "data": [
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "EXTERNAL LINKS",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "Metabolights accession", "iri": None},
                        "measurement": {"value": "MTBLSXXXXX", "iri": None},
                    },
                    {
                        "marker": {"value": "ENA Run ID", "iri": None},
                        "measurement": {"value": "ERR4918394", "iri": None},
                    },
                    {
                        "marker": {"value": "ENA Experiment ID", "iri": None},
                        "measurement": {"value": "ERX4783303", "iri": None},
                    },
                ],
            },
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "SAMPLE",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "Personnel", "iri": None},
                        "measurement": {"value": "Captain Donut", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Host %", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Box", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "ng used for library build", "iri": None},
                        "measurement": {"value": "399.6", "iri": None},
                        "measurement_units": {"value": "ng", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "No. Non-host reads", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Comments", "iri": None},
                        "measurement": {"value": "NA", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Position", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Omics", "iri": None},
                        "measurement": {"value": "Metagenomics", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Storage 2D tube row", "iri": None},
                        "measurement": {"value": "5", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Observations", "iri": None},
                        "measurement": {"value": "NA", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Index PCR cycles", "iri": None},
                        "measurement": {"value": "9", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Row", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "No. host reads", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Pool", "iri": None},
                        "measurement": {"value": "S-MG-P37-502", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "2D Tube column", "iri": None},
                        "measurement": {"value": "B", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Empty", "iri": None},
                        "measurement": {"value": "false", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sequencing company", "iri": None},
                        "measurement": {"value": "BGI", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "No. Quality-filtered reads", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                ],
            },
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "HEAVY METALS",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "Lead", "iri": None},
                        "measurement": {"value": "<0.006", "iri": None},
                        "measurement_units": {"value": "mg/kg dw", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Selenium", "iri": None},
                        "measurement": {"value": "0.33", "iri": None},
                        "measurement_units": {"value": "mg/kg dw", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Quicksilver", "iri": None},
                        "measurement": {"value": "0.03", "iri": None},
                        "measurement_units": {"value": "mg/kg dw", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Total Arsenic", "iri": None},
                        "measurement": {"value": "0.89", "iri": None},
                        "measurement_units": {"value": "mg/kg dw", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Organ", "iri": None},
                        "measurement": {"value": "muscle", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Cadmium", "iri": None},
                        "measurement": {"value": "<0.001", "iri": None},
                        "measurement_units": {"value": "mg/kg dw", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                ],
            },
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "TRIAL",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "Trial end", "iri": None},
                        "measurement": {"value": "2021-12-15", "iri": None},
                    },
                    {
                        "marker": {"value": "Trial start", "iri": None},
                        "measurement": {"value": "2021-10-05", "iri": None},
                    },
                    {
                        "marker": {"value": "Trial description", "iri": None},
                        "measurement": {
                            "value": "Trial A: Seaweed-dose response",
                            "iri": None,
                        },
                    },
                    {
                        "marker": {"value": "Trial code", "iri": None},
                        "measurement": {"value": "SA", "iri": None},
                    },
                    {
                        "marker": {"value": "Sample code", "iri": None},
                        "measurement": {"value": "SA01.02C1a", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                ],
            },
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "TREATMENT",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "Total end weight", "iri": None},
                        "measurement": {"value": "227671", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Target Fat", "iri": None},
                        "measurement": {"value": "26.7", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Total mid sampling biomass", "iri": None},
                        "measurement": {"value": "5871", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Total start biomass ", "iri": None},
                        "measurement": {"value": "144137", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Soy SPC", "iri": None},
                        "measurement": {"value": "20.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Biomass dead fish", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Target Moisture", "iri": None},
                        "measurement": {"value": "6.0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Fermented Algae (added in in oil coating)",
                            "iri": None,
                        },
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Average end weight", "iri": None},
                        "measurement": {"value": "570.6", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Water Change", "iri": None},
                        "measurement": {"value": "0.50", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Feed conversion ratio", "iri": None},
                        "measurement": {"value": "1.00", "iri": None},
                        "measurement_units": {
                            "value": "kg feed/ kg fish weight gain",
                            "iri": None,
                        },
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Thermal growth coefficient", "iri": None},
                        "measurement": {"value": "2.16", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Yttrium", "iri": None},
                        "measurement": {"value": "0.10", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Vit + min + AA", "iri": None},
                        "measurement": {"value": "4.70", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Fish Meal", "iri": None},
                        "measurement": {"value": "15.0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Mortality (No. of fish)", "iri": None},
                        "measurement": {"value": "1", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Lecithin Soy", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Fish Oil", "iri": None},
                        "measurement": {"value": "17.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Pea Protein", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Standard growth rate", "iri": None},
                        "measurement": {"value": "1.13", "iri": None},
                        "measurement_units": {"value": "%/day", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Target Energy (crude)", "iri": None},
                        "measurement": {"value": "23.8", "iri": None},
                        "measurement_units": {"value": "MJ/kg", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Wheat Gluten", "iri": None},
                        "measurement": {"value": "12.60", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Mid sampling (No. of fish)", "iri": None},
                        "measurement": {"value": "15", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Target Protein (crude)", "iri": None},
                        "measurement": {"value": "43.2", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Guar Meal", "iri": None},
                        "measurement": {"value": "13.0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Analyzed Energy (bomb calorimetry)",
                            "iri": None,
                        },
                        "measurement": {"value": "22.50", "iri": None},
                        "measurement_units": {"value": "MJ/kg", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Analyzed Fat", "iri": None},
                        "measurement": {"value": "27.0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "End of sampling (No. of fish)",
                            "iri": None,
                        },
                        "measurement": {"value": "60", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Average start weight", "iri": None},
                        "measurement": {"value": "300.3", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Analyzed Moisture", "iri": None},
                        "measurement": {"value": "5.4", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Notes", "iri": None},
                        "measurement": {"value": "NA", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Analyzed Protein", "iri": None},
                        "measurement": {"value": "42.8", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Start of sampling (No. of fish)",
                            "iri": None,
                        },
                        "measurement": {"value": "480", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Wheat", "iri": None},
                        "measurement": {"value": "11.00", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sanford Blue Mussel Meal", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Analyzed Yttrium", "iri": None},
                        "measurement": {"value": "423", "iri": None},
                        "measurement_units": {"value": "mg/kg", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Rapeseed Oil", "iri": None},
                        "measurement": {"value": "5.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Total end of sampling biomass",
                            "iri": None,
                        },
                        "measurement": {"value": "36883", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                ],
            },
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "FATTY ACIDS",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "22:1n-11", "iri": None},
                        "measurement": {"value": "1.87", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "21:5n-3", "iri": None},
                        "measurement": {"value": "0.15", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Myristic acid 14:0", "iri": None},
                        "measurement": {"value": "1.66", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Stearidonic acid 18:4n-3", "iri": None},
                        "measurement": {"value": "0.56", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Linoleic acid 18:2n-6", "iri": None},
                        "measurement": {"value": "12.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Docosapentaenoic acid 22:5n-3 (DPA)",
                            "iri": None,
                        },
                        "measurement": {"value": "1.00", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Stearidonic acid 18:4n-3", "iri": None},
                        "measurement": {"value": "0.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Gamma-Linolenic acid 18:3n-6",
                            "iri": None,
                        },
                        "measurement": {"value": "0.10", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Vaccenic acid 18:1n-7", "iri": None},
                        "measurement": {"value": "3.40", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Caprylic acid 8:0", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 20:1", "iri": None},
                        "measurement": {"value": "2.31", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Paullinic acid 20:1n-7", "iri": None},
                        "measurement": {"value": "0.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Myristoleic acid 14:1n-9", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum saturated", "iri": None},
                        "measurement": {"value": "16.60", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Margaric acid 17:0", "iri": None},
                        "measurement": {"value": "0.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum saturated", "iri": None},
                        "measurement": {"value": "12.00", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum unidentified", "iri": None},
                        "measurement": {"value": "1.70", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Eicosadienoic acid 20:2n-6", "iri": None},
                        "measurement": {"value": "0.90", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Nervonic acid 24:1n-9", "iri": None},
                        "measurement": {"value": "0.40", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "21:5n-3", "iri": None},
                        "measurement": {"value": "0.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Eicosatrienoic acid 20:3n-3", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Caproic acid 6:0", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Eicosatetraenoic acid 20:4n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "0.70", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum n-6", "iri": None},
                        "measurement": {"value": "15.00", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Lignoceric acid 24:0", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Arachidonic acid 20:4n-6 (ARA)",
                            "iri": None,
                        },
                        "measurement": {"value": "0.70", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Tetracosapentaenoic acid 24:5n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "0.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Oleic acid 18:1n-9", "iri": None},
                        "measurement": {"value": "24.41", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Eicosatetraenoic acid 20:4n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "0.47", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "16:4n-3", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Capric acid 10:0", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum identified", "iri": None},
                        "measurement": {"value": "71.00", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 22:1", "iri": None},
                        "measurement": {"value": "3.10", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Organ", "iri": None},
                        "measurement": {"value": "muscle", "iri": None},
                    },
                    {
                        "marker": {"value": "Behenic acid 22:0", "iri": None},
                        "measurement": {"value": "0.10", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum fatty acids", "iri": None},
                        "measurement": {"value": "72.20", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Paullinic acid 20:1n-7", "iri": None},
                        "measurement": {"value": "0.13", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Pentadecylic acid 15:0", "iri": None},
                        "measurement": {"value": "0.13", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Arachidic acid 20:0", "iri": None},
                        "measurement": {"value": "0.18", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "n-3/n-6", "iri": None},
                        "measurement": {"value": "1.20", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Lignoceric acid 24:0", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Osbond acid 22:5n-6", "iri": None},
                        "measurement": {"value": "0.08", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Adrenic acid 22:4n-6", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum EPA+DHA", "iri": None},
                        "measurement": {"value": "7.77", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum polyunsaturated", "iri": None},
                        "measurement": {"value": "24.00", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Hexadecatrienoic acid 16:3n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Hypogeic acid 16:1n-9", "iri": None},
                        "measurement": {"value": "0.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Tetracosahexaenoic acid 24:6n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "0.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Palmitoleic acid 16:1n-7", "iri": None},
                        "measurement": {"value": "2.50", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Eicosenoic acid 20:1n-9", "iri": None},
                        "measurement": {"value": "2.87", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Gamma-Linolenic acid 18:3n-6",
                            "iri": None,
                        },
                        "measurement": {"value": "0.11", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Gadoleic acid 20:1n-11", "iri": None},
                        "measurement": {"value": "0.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Adrenic acid 22:4n-6", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Linoleic acid 18:2n-6", "iri": None},
                        "measurement": {"value": "9.22", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Tetracosahexaenoic acid 24:6n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "0.15", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "16:2n-4", "iri": None},
                        "measurement": {"value": "0.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Eicosenoic acid 20:1n-9", "iri": None},
                        "measurement": {"value": "4.00", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Hypogeic acid 16:1n-9", "iri": None},
                        "measurement": {"value": "0.18", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Alpha-Linolenic acid 18:3n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "3.04", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Palmitic acid 16:0", "iri": None},
                        "measurement": {"value": "10.70", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Mead acid 20:3n-9", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Di-homo-gamma-linolenic acid 20:3n-6",
                            "iri": None,
                        },
                        "measurement": {"value": "0.24", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Arachidic acid 20:0", "iri": None},
                        "measurement": {"value": "0.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Caprylic acid 8:0", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Myristoleic acid 14:1n-9", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "n-6/n-3", "iri": None},
                        "measurement": {"value": "0.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Eicosapentaenoic acid 20:5n-3 (EPA)",
                            "iri": None,
                        },
                        "measurement": {"value": "2.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Nervonic acid 24:1n-9", "iri": None},
                        "measurement": {"value": "0.27", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 18:1", "iri": None},
                        "measurement": {"value": "27.10", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Arachidonic acid 20:4n-6 (ARA)",
                            "iri": None,
                        },
                        "measurement": {"value": "0.50", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 16:1", "iri": None},
                        "measurement": {"value": "1.96", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Eicosapentaenoic acid 20:5n-3 (EPA)",
                            "iri": None,
                        },
                        "measurement": {"value": "2.04", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "n-6/n-3", "iri": None},
                        "measurement": {"value": "0.80", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum monounsaturate", "iri": None},
                        "measurement": {"value": "34.80", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Pentadecylic acid 15:0", "iri": None},
                        "measurement": {"value": "0.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum n-3", "iri": None},
                        "measurement": {"value": "18.10", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Palmitoleic acid 16:1n-7", "iri": None},
                        "measurement": {"value": "1.78", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Eicosadienoic acid 20:2n-6", "iri": None},
                        "measurement": {"value": "0.68", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum n-6", "iri": None},
                        "measurement": {"value": "10.80", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "22:1n-11", "iri": None},
                        "measurement": {"value": "2.60", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Myristic acid 14:0", "iri": None},
                        "measurement": {"value": "2.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Docosahexaenoic acid 22:6n-3 (DHA)",
                            "iri": None,
                        },
                        "measurement": {"value": "5.74", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 20:1", "iri": None},
                        "measurement": {"value": "4.50", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Stearic acid 18:0", "iri": None},
                        "measurement": {"value": "2.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum monounsaturate", "iri": None},
                        "measurement": {"value": "48.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "18:1n-11", "iri": None},
                        "measurement": {"value": "0.22", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Capric acid 10:0", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Eicosatrienoic acid 20:3n-3", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Docosapentaenoic acid 22:5n-3 (DPA)",
                            "iri": None,
                        },
                        "measurement": {"value": "0.76", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Erucic acid 22:1n-9", "iri": None},
                        "measurement": {"value": "0.60", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 18:1", "iri": None},
                        "measurement": {"value": "37.50", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Oleic acid 18:1n-9", "iri": None},
                        "measurement": {"value": "33.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Tetracosapentaenoic acid 24:5n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "0.14", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Hexadecatrienoic acid 16:3n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum EPA+DHA", "iri": None},
                        "measurement": {"value": "10.80", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Stearic acid 18:0", "iri": None},
                        "measurement": {"value": "2.04", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Caproic acid 6:0", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum identified", "iri": None},
                        "measurement": {"value": "98.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Erucic acid 22:1n-9", "iri": None},
                        "measurement": {"value": "0.40", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Lauric acid 12:0", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Palmitic acid 16:0", "iri": None},
                        "measurement": {"value": "7.73", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "18:1n-11", "iri": None},
                        "measurement": {"value": "0.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum polyunsaturated", "iri": None},
                        "measurement": {"value": "33.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Gadoleic acid 20:1n-11", "iri": None},
                        "measurement": {"value": "0.22", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Osbond acid 22:5n-6", "iri": None},
                        "measurement": {"value": "0.10", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "n-3/n-6", "iri": None},
                        "measurement": {"value": "1.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Behenic acid 22:0", "iri": None},
                        "measurement": {"value": "0.10", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Margaric acid 17:0", "iri": None},
                        "measurement": {"value": "0.12", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 16:1", "iri": None},
                        "measurement": {"value": "2.70", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Di-homo-gamma-linolenic acid 20:3n-6",
                            "iri": None,
                        },
                        "measurement": {"value": "0.30", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "16:4n-3", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum 22:1", "iri": None},
                        "measurement": {"value": "2.27", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum fatty acids", "iri": None},
                        "measurement": {"value": "100.00", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Alpha-Linolenic acid 18:3n-3",
                            "iri": None,
                        },
                        "measurement": {"value": "4.20", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Docosahexaenoic acid 22:6n-3 (DHA)",
                            "iri": None,
                        },
                        "measurement": {"value": "7.90", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Lauric acid 12:0", "iri": None},
                        "measurement": {"value": "<0.1", "iri": None},
                        "measurement_units": {"value": "%", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum n-3", "iri": None},
                        "measurement": {"value": "13.00", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Vaccenic acid 18:1n-7", "iri": None},
                        "measurement": {"value": "2.46", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Sum unidentified", "iri": None},
                        "measurement": {"value": "1.22", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "16:2n-4", "iri": None},
                        "measurement": {"value": "0.16", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Mead acid 20:3n-9", "iri": None},
                        "measurement": {"value": "<0.01", "iri": None},
                        "measurement_units": {"value": "mg/g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                ],
            },
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "TANK",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "Mid sampling (No. of fish)", "iri": None},
                        "measurement": {"value": "5", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "End of sampling (No. of fish)",
                            "iri": None,
                        },
                        "measurement": {"value": "20", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Total end of sampling biomass",
                            "iri": None,
                        },
                        "measurement": {"value": "12081", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Total mid sampling biomass", "iri": None},
                        "measurement": {"value": "1947", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Total start biomass ", "iri": None},
                        "measurement": {"value": "47944", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Total end weight", "iri": None},
                        "measurement": {"value": "76565", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Average end weight", "iri": None},
                        "measurement": {"value": "575.7", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Tank code", "iri": None},
                        "measurement": {"value": "SA01", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "LetSea Tank code", "iri": None},
                        "measurement": {"value": "18", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Average start weight", "iri": None},
                        "measurement": {"value": "299.7", "iri": None},
                        "measurement_units": {"value": "g", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Mortality (No. of fish)", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Standard growth rate", "iri": None},
                        "measurement": {"value": "1.18", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "Start of sampling (No. of fish)",
                            "iri": None,
                        },
                        "measurement": {"value": "160", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Feed conversion ratio", "iri": None},
                        "measurement": {"value": "1.00", "iri": None},
                        "measurement_units": {
                            "value": "feed mass/fish weight gain",
                            "iri": None,
                        },
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Notes", "iri": None},
                        "measurement": {
                            "value": "LetSea tank ID for source fishes: 101",
                            "iri": None,
                        },
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {
                            "value": "The thermal growth coefficient",
                            "iri": None,
                        },
                        "measurement": {"value": "2.26", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                ],
            },
            {
                "domain": None,
                "webinSubmissionAccountId": "Webin-test",
                "type": "HISTOLOGY",
                "schema": None,
                "content": [
                    {
                        "marker": {"value": "Villous height", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "um", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                    {
                        "marker": {"value": "Villous width", "iri": None},
                        "measurement": {"value": "0", "iri": None},
                        "measurement_units": {"value": "um", "iri": None},
                        "partner": {
                            "value": "DONUT",
                            "iri": "https://www.example.com/donut/",
                        },
                    },
                ],
            },
        ],
    }


@pytest.fixture()
def salmon_submitted_checklist(salmon_sample):
    return f"""
    <SAMPLE_SET>
      <SAMPLE accession="{salmon_sample.accession}" alias="{salmon_sample.title}"
               center_name="UNIVERSITY OF DONUTS">
          <IDENTIFIERS>
             <PRIMARY_ID>{salmon_sample.accession}</PRIMARY_ID>
             <SUBMITTER_ID namespace="UNIVERSITY OF DONUTS">{salmon_sample.accession}</SUBMITTER_ID>
          </IDENTIFIERS>
          <TITLE>{salmon_sample.title}</TITLE>
          <SAMPLE_NAME>
             <TAXON_ID>1602388</TAXON_ID>
             <SCIENTIFIC_NAME>fish gut metagenome</SCIENTIFIC_NAME>
          </SAMPLE_NAME>
          <DESCRIPTION>Salmon metagenomic DNA data from fish living in a donut</DESCRIPTION>
          <SAMPLE_ATTRIBUTES>
             <SAMPLE_ATTRIBUTE>
                <TAG>adapters</TAG>
                <VALUE>AAGTCGGAGGCCAAGCGGTCTTAGGAAGACAA;GAACGACATGGCTACGATCCGACTT</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>collection date</TAG>
                <VALUE>2019-06-11</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>geographic location (country and/or sea)</TAG>
                <VALUE>Norway</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>geographic location (latitude)</TAG>
                <VALUE>66.079905</VALUE>
                <UNITS>DD</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>geographic location (longitude)</TAG>
                <VALUE>12.587848</VALUE>
                <UNITS>DD</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>geographic location (region and locality)</TAG>
                <VALUE>Dønna; Nordland county</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host body site</TAG>
                <VALUE>Distal gut content</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host common name</TAG>
                <VALUE>Atlantic salmon</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host diet</TAG>
                <VALUE>Fermented algae meal (added in in oil coating)</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host diet treatment</TAG>
                <VALUE>Tiger: SA Control</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host disease status</TAG>
                <VALUE>Wounded:-</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host scientific name</TAG>
                <VALUE>Salmo salar</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host subject id</TAG>
                <VALUE>SA01.02</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host taxid</TAG>
                <VALUE>8030</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host total mass</TAG>
                <VALUE>290.4</VALUE>
                <UNITS>g</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>nucleic acid extraction</TAG>
                <VALUE>D-rex protocol</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>pcr primers</TAG>
                <VALUE>N/A</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>project name</TAG>
                <VALUE>HoloFood Salmon - Metagenomic DNA</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>reference host genome for decontamination</TAG>
                <VALUE>GCA_000000000.0</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>sample storage buffer</TAG>
                <VALUE>Shield</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>sample storage container</TAG>
                <VALUE>2ml E-matrix</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>sample storage location</TAG>
                <VALUE>UCPH</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>sample storage temperature</TAG>
                <VALUE>-20</VALUE>
                <UNITS>°C</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>sample volume or weight for DNA extraction</TAG>
                <VALUE>0.2</VALUE>
                <UNITS>mL</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>sequencing method</TAG>
                <VALUE>MGISEQ-2000</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>trial timepoint</TAG>
                <VALUE>0</VALUE>
                <UNITS>days</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host storage container temperature</TAG>
                <VALUE>12.76</VALUE>
                <UNITS>°C</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host storage container pH</TAG>
                <VALUE>7.05</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host gutted mass</TAG>
                <VALUE>246.6</VALUE>
                <UNITS>g</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host length</TAG>
                <VALUE>29.5</VALUE>
                <UNITS>cm</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host diet treatment concentration</TAG>
                <VALUE>0</VALUE>
                <UNITS>% mass</UNITS>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>host storage container</TAG>
                <VALUE>LetSea Tank: Tiger</VALUE>
             </SAMPLE_ATTRIBUTE>
             <SAMPLE_ATTRIBUTE>
                <TAG>ENA-CHECKLIST</TAG>
                <VALUE>ERC000052</VALUE>
             </SAMPLE_ATTRIBUTE>
          </SAMPLE_ATTRIBUTES>
      </SAMPLE>
    </SAMPLE_SET>
    """


@pytest.fixture(scope="class")
def LiveTests(request):
    class Fixtures:
        pass

    Fixtures.projects = [
        Project.objects.create(accession="PRJTESTING", title="HoloFood Donut and Fish")
    ]

    Fixtures.samples = [
        Sample.objects.create(
            accession="SAMEA00000002",
            project=Fixtures.projects[0],
            title="HF_DONUT.SALMON.1",
            system=Sample.SALMON,
        )
    ]

    # set a class attribute on the invoking test context
    request.cls.hf_fixtures = Fixtures()
