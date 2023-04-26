import pytest

from holofood.management.commands.generate_dev_data import METAB_FILES
from holofood.models import (
    Sample,
    SampleMetadataMarker,
    AnalysisSummary,
    GenomeCatalogue,
    Genome,
    ViralCatalogue,
    ViralFragment,
    SampleStructuredDatum,
    Animal,
)
from holofood.utils import holofood_config


@pytest.fixture()
def salmon_animal():
    return Animal.objects.create(
        accession="SAMEG04",
        system=Animal.SALMON,
    )


@pytest.fixture()
def chicken_animal():
    return Animal.objects.create(
        accession="SAMEG01",
        system=Animal.CHICKEN,
    )


@pytest.fixture()
def salmon_metagenomic_sample(salmon_animal):
    return Sample.objects.create(
        accession="SAMEA00000002",
        title="HF_DONUT.SALMON.METAG",
        animal=salmon_animal,
        sample_type=Sample.METAGENOMIC_ASSEMBLY,
    )


@pytest.fixture()
def salmon_metabolomic_sample(salmon_animal):
    return Sample.objects.create(
        accession="SAMEA00000003",
        animal=salmon_animal,
        sample_type=Sample.METABOLOMIC,
        title="HF_DONUT.SALMON.METAB",
        metabolights_files=METAB_FILES,
    )


@pytest.fixture()
def salmon_histological_sample(salmon_animal):
    return Sample.objects.create(
        accession="SAMEA00000004",
        animal=salmon_animal,
        sample_type=Sample.HISTOLOGICAL,
        title="HF_DONUT.SALMON.HIST",
    )


@pytest.fixture()
def salmon_host_sample(salmon_animal):
    return Sample.objects.create(
        accession="SAMEA00000005",
        animal=salmon_animal,
        sample_type=Sample.HOST_GENOMIC,
        title="HF_DONUT.SALMON.HOST",
    )


@pytest.fixture()
def chicken_metagenomic_sample(chicken_animal):
    return Sample.objects.create(
        accession="SAMEA00000006",
        title="HF_DONUT.CHICKEN.METAG",
        animal=chicken_animal,
        sample_type=Sample.METAGENOMIC_ASSEMBLY,
    )


@pytest.fixture()
def chicken_metabolomic_sample(chicken_animal):
    return Sample.objects.create(
        accession="SAMEA00000007",
        animal=chicken_animal,
        sample_type=Sample.METABOLOMIC,
        title="HF_DONUT.CHICKEN.METAB",
        metabolights_files=METAB_FILES,
    )


@pytest.fixture()
def chicken_histological_sample(chicken_animal):
    return Sample.objects.create(
        accession="SAMEA00000008",
        animal=chicken_animal,
        sample_type=Sample.HISTOLOGICAL,
        title="HF_DONUT.CHICKEN.HIST",
    )


@pytest.fixture()
def chicken_host_sample(chicken_animal):
    return Sample.objects.create(
        accession="SAMEA00000009",
        animal=chicken_animal,
        sample_type=Sample.HOST_GENOMIC,
        title="HF_DONUT.CHICKEN.HOST",
    )


@pytest.fixture()
def salmon_animal_structureddata_response(salmon_animal):
    return {
        "accession": salmon_histological_sample.accession,
        "create": "2022-05-05T14:16:35.502Z",
        "update": "2022-05-05T14:16:35.506Z",
        "data": [
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
        ],
    }


@pytest.fixture()
def salmon_metabolomic_structureddata_response(salmon_metabolomic_sample):
    return {
        "accession": salmon_histological_sample.accession,
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
                        "measurement": {"value": "MTBLSDONUT", "iri": None},
                    },
                ],
            }
        ],
    }


@pytest.fixture()
def salmon_histological_structureeddata_response(salmon_histological_sample):
    return {
        "accession": salmon_histological_sample.accession,
        "create": "2022-05-05T14:16:35.502Z",
        "update": "2022-05-05T14:16:35.506Z",
        "data": [
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
def salmon_metagenomic_structureddata_response(salmon_metagenomic_sample):
    return {
        "accession": salmon_histological_sample.accession,
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
                        "marker": {"value": "ENA Run ID", "iri": None},
                        "measurement": {"value": "ERR4918394", "iri": None},
                    },
                    {
                        "marker": {"value": "ENA Experiment ID", "iri": None},
                        "measurement": {"value": "ERX4783303", "iri": None},
                    },
                ],
            },
        ],
    }


@pytest.fixture()
def salmon_sample_metabolights_response(salmon_sample):
    return {
        "sample_files": [
            {
                "file_name": "donut.zip",
                "reliability": "1.0",
                "sample_name": salmon_sample.accession,
            },
            {
                "file_name": "donut.nmrML",
                "reliability": "1.0",
                "sample_name": salmon_sample.accession,
            },
        ]
    }


@pytest.fixture()
def salmon_submitted_checklist(salmon_animal):
    return f"""
    <SAMPLE_SET>
      <SAMPLE accession="{salmon_animal.accession}" alias="{salmon_animal.animal_code}"
               center_name="UNIVERSITY OF DONUTS">
          <IDENTIFIERS>
             <PRIMARY_ID>{salmon_animal.accession}</PRIMARY_ID>
             <SUBMITTER_ID namespace="UNIVERSITY OF DONUTS">{salmon_animal.accession}</SUBMITTER_ID>
          </IDENTIFIERS>
          <TITLE>SALMON ANIMAL</TITLE>
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


def create_genome_objects() -> GenomeCatalogue:
    catalogue, _ = GenomeCatalogue.objects.get_or_create(
        id="hf-mag-cat-v1",
        defaults={
            "title": "HoloFood MAG Catalogue v1.0",
            "biome": "Donut Surface",
            "related_mag_catalogue_id": "donuts-v1-0",
            "system": "chicken",
        },
    )

    Genome.objects.get_or_create(
        accession="MGYG999",
        defaults={
            "cluster_representative": "MGYG001",
            "catalogue": catalogue,
            "taxonomy": "Root > Foods > Donuts > Sugar Monster",
            "metadata": {},
        },
    )
    return catalogue


def salmon_metagenomics_analyses_response(salmon_metagenomic_sample):
    return {
        "data": [
            {
                "attributes": {
                    "accession": "MGYA00000001",
                    "analysis-status": "completed",
                    "analysis-summary": [
                        {"key": "Submitted nucleotide sequences", "value": "16576"},
                        {
                            "key": "Nucleotide sequences after format-specific filtering",
                            "value": "15559",
                        },
                        {
                            "key": "Nucleotide sequences after length filtering",
                            "value": "15559",
                        },
                        {
                            "key": "Nucleotide sequences after undetermined bases filtering",
                            "value": "15559",
                        },
                        {"key": "Predicted SSU sequences", "value": "15566"},
                        {"key": "Predicted LSU sequences", "value": "0"},
                    ],
                    "complete-time": "2020-07-25T20:30:41",
                    "experiment-type": "amplicon",
                    "instrument-model": "454 GS FLX Titanium",
                    "instrument-platform": "LS454",
                    "pipeline-version": "5.0",
                },
                "id": "MGYA00000001",
                "links": {
                    "self": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001?format=json"
                },
                "relationships": {
                    "antismash-gene-clusters": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/antismash-gene-clusters?format=json"
                        }
                    },
                    "assembly": {"data": None},
                    "downloads": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/downloads?format=json"
                        }
                    },
                    "genome-properties": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/genome-properties?format=json"
                        }
                    },
                    "go-slim": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/go-slim?format=json"
                        }
                    },
                    "go-terms": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/go-terms?format=json"
                        }
                    },
                    "interpro-identifiers": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/interpro-identifiers?format=json"
                        }
                    },
                    "run": {
                        "data": {"id": "ERR227209", "type": "runs"},
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/runs/ERR4918394?format=json"
                        },
                    },
                    "sample": {
                        "data": {"id": "ERS211823", "type": "samples"},
                        "links": {
                            "related": f"https://www.ebi.ac.uk/metagenomics/api/v1/samples/{salmon_metagenomic_sample.accession}?format=json"
                        },
                    },
                    "study": {
                        "data": {"id": "MGYS00005566", "type": "studies"},
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYD00000001?format=json"
                        },
                    },
                    "taxonomy": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/taxonomy?format=json"
                        }
                    },
                    "taxonomy-itsonedb": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/taxonomy/itsonedb?format=json"
                        }
                    },
                    "taxonomy-itsunite": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/taxonomy/unite?format=json"
                        }
                    },
                    "taxonomy-lsu": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/taxonomy/lsu?format=json"
                        }
                    },
                    "taxonomy-ssu": {
                        "links": {
                            "related": "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00000001/taxonomy/ssu?format=json"
                        }
                    },
                },
                "type": "analysis-jobs",
            }
        ],
        "links": {
            "first": "https://www.ebi.ac.uk/metagenomics/api/v1/runs/ERR4918394/analyses?format=json&page=1",
            "last": "https://www.ebi.ac.uk/metagenomics/api/v1/runs/ERR4918394/analyses?format=json&page=1",
            "next": None,
            "prev": None,
        },
        "meta": {"pagination": {"count": 1, "page": 1, "pages": 1}},
    }


def create_viral_objects() -> ViralCatalogue:
    catalogue = ViralCatalogue.objects.create(
        id="hf-donut-vir-cat-v1",
        title="HoloFood Donut Viral Catalogue v1",
        biome="Donut Surface",
        related_genome_catalogue=create_genome_objects(),
        system="chicken",
    )
    rep = ViralFragment.objects.create(
        id="MGYC001-start-1000-end-2000",
        catalogue=catalogue,
        start_within_contig=1000,
        end_within_contig=2000,
        contig_id="MGYC001",
        viral_type=ViralFragment.PROPHAGE,
        mgnify_analysis_accession="MGYA001",
        gff="MGYC001\tViPhOg\tCDS\t1020\t1990\t.\t-\t.\tID=MGYC001;viphog=ViPhOG1\n",
    )
    ViralFragment.objects.create(
        id="MGYC001-start-3000-end-4000",
        catalogue=catalogue,
        start_within_contig=3000,
        end_within_contig=4000,
        contig_id="MGYC001",
        viral_type=ViralFragment.PROPHAGE,
        mgnify_analysis_accession="MGYA001",
        cluster_representative=rep,
        gff="MGYC001\tViPhOg\tCDS\t3020\t3090\t.\t-\t.\tID=MGYC001;viphog=ViPhOG2\n",
    )
    return catalogue


def mgnify_contig_response(viral_fragment: ViralFragment) -> str:
    return f""">{viral_fragment.contig_id}
TACCACATGCAACAAGAGCAGAAAACTCGCCCAACGAATGACCAGCGACCATGTCCGGAGCGAAGTCCTCTATACATTTTGCCATTACAACGGAATGTAAGAAGACCGCCGGTTGGGTAACCTTAGTTTGCTTAAGGTCTTCTGCAGTACCATTGAACATAATATCTGAAATAGAAAATCCAAGAATCTCATCAGCCTGTTCAAACATAGAACGTGCGATAGGATTTGTTTCATATAGTTCCTTGCCCATTCCGGGGAATTGGGAGCCTTGACCAGGGAAAATGTATGCTTTTTTCACTTTATAAATTATTTGTTTCAACTTAAATATCCATTTTGTACGGGTCTATGTCCAGCATTTCATCAATATTGATTATACCATAGTTTTGGGCCTTAATTTCCTCTATAAGCATTTGTAGTAATTCATCAGCCCCTTTGCATCTATCATGCAATAGAATTATAGCACCATTATGCAACCGTCTTAAAACACGATTCAATATATCTTGTCTTGGTGTATCTTCATCTGTATCCAGTGACCTGACACTCCAACCTATACACGTATAATCTGTTTCGCTTATCGCATCTGCAATCAGTGGATTTGTTACGCCAAACGGAGGACGAAACAATGACATTCTTTTACCCGTAATAGAATATATAAGACTATCACATTTACTTAATTCACTATAAATATCCTCGGAGGATTGCAGTGGAAAGGTACATGAATGATTCCAACTATGGTTGCCAATAATATGGCCCTCATCTATAATTCGTGTAACTAACTCGGGATATCTACTGGCATTGTTTCCAATAAGAAAAAAAGTAGCTTTCAGATTATGATGCTTCAGAATATCCAGAATCTTTGGTGTCATTTCTTCATTTGGGCCGTCATCAAATGTCAATGTAACGCAACGTTTAGTATCAGATCCATGGCATAAGCAATTCATGTACACTCCGCTGTCGATATCTGAAGAAGCCCAATATAGAAATCCCAAAATACAGACTGAAATCAAACACCCAGATAGTAGGACTCTTCTTATATACAATTTATTCAAGTGCATATTTAGAATTTAAATTTTGCAGAGATAGTAGGTGTGAATCCCATTAGTCCCTCTACATCGTATTTAATACGACCCTCTGACACCATCATTCCTATTGTCGGACGTAAATCCGCAGACAGTGTCAATGGAAACCAGAAATTATACTCAAGTCCAGCCTGTCCTGTAACACCAAAGCAAAAAGCCTTATATGTATTGAAGCCAGAGCCCATCGATAGACCTGGTCCGGCATAAAAATTCCAGTCTCCCCTACTTGTCCAACTAGGAGACATAATTACCATATTATATGTTGCAGTAAGCCTTAGTGTACCAGCCGAACGTTTGGCTACATCATAGTAATGATCAATATAATCATTGGTGTAGTCAGAAGAAGCTAATAGACCACAGTGATATCCAAAATTCAGTTCTATAAAATTACCTTTTGAAACACCATGCTGATATGTTAAGGTTTCTGACCAACCTAAGCTTCCACCTACTGATCTCGGTTGAGCCAATGCAGTTGCGACAATAAAAGTTGAAATGAATAGCAAAAATATCTTTTTCATAAAATTCTTGTTTTTGTTTAAAAAGGGCGTGACTCGGTTTCACGCCCTTACATGCAGACAAAATAACGGTGACGCATTAACCAAAAAAGATCATTCTCATCTTGTCCACATGGGTTAAGAATTATTCGCTTGTGTGCTATATATTATGTTTAATAAAATCTCTTACTAGAGACATAATCTTGTTTTTATCAGCATTCATAAAGTGTCCCTCATCTTCTAATAAATAAAGTTCACTATCTGAATATAGGTCGTGATATTTTTCACTATATGAATATGGGACAATTTTATCGCGCTTACCATGAATTAGGCATACCTTTCCTGTATACTTGCATGACACTTCATAAACTGGGAGTTTTTGAGCTGCAAGAATAAACTTACGTCCAAGCTTATGAAACATCACATTAACATACTCAGGTGGGTTAGAAGCGTCATATTTTTTACCCATGCATTGACCAGCTATTGCATCATCTTTAAGAACAGCAGCAGGAGCGAGTAGTACTAGACATTTAGGCTTCTTTTCCTCTGATTCCAATTCGCCAGCTAGCATACCAGAGATTACACCACCTTGTGAGTGACCAATAAATATTGTGTCAGTTACGTATGGAAGAGTATTAACATATCTGAAAACGGCCTTTGCATCTTCAATCTCATTAGCTATTGTCATGTCAATAAACTCCCCTTCACTTTTTCCGTGAGCATTAAAGTCAAAACATATGGAAGCGATACCCTCTTTTGCTAATGTCTCAGCAAGCATTGGAACTGGATACATTTTCTTGCTTGACATAAATCCATGCATAAGAATAGCCATCGGGCATTTGTCTTTTTTAGGATTGAATCCATTGGGTAACGTAATCTTTGTCGAGATCCCTCCTTGTGATCCAAAGACAATAAACTCTTCTTTACGGGGAGCAAGAATCCTTTTAATTTTACCGAGAAGTTTTTTCATAATGCGATAATTATTTATTCGTTTTATAAAATTTCCTGTCTAATTTTCCATTATAGGTACGTTGTATTGTATCGACTGCCTCGTAATAGGTTGGGACTTTGTGAGGTTCTAATTTTGATTTAATGTGAACGGCAATAGACCTTTTATCCAATTCACAGTTCTCAGCCAATACGACAAGAAGCTTAAGTACTGTACCTATGACCGGATGTGTCGCAGCGATACAGATACAATCCTTTATCATCGGATGAGACGCAGCTGCATTTTCAACTTCAGAAGGATCCACCTTAAATCCTCCGACATTGATTACATCTCCCTGACGACCTTTAAGGTGTATCAGTCCTTCTGAATCAACGTATCCCAAGTCAGCACTGTAAATCTTACCGTCCTTAAGTATGCGAGCTGTATTTTCGGGATCAGCCACATAGCCACTCATGATAGTGAGTCCTGAGACGATAATGTTTCCCTCTGGCGTAACTTCAACAGTGGAGTTTTTCATAGGACGTCCTATACAACCTTCCATATATTTCCCATCATTGAAGTTATAGGTACAGACTGCACCAATCTCTGTTCCTCCCAATGTATTATAAAGGCGGGATTTTGGCAACGCTTTGCTGAGCATTTCCATATCGTGCTGAGTGATTGGAGCAGCTCCAGTTTCTATAAAATCAATCTTATCAGCGAGTTGACATAGTCTCTCATATGAGAACTGCATGATCAAACGGATACTAGCAGGTACGAGGAATGTTGCAAATTTCTTGAACGGAAGTTCAAAGACATCGAAAAACGCGTTAATGTCTTTAAGACCATCAAGAATGCATATTGTACCACCAACTGTAAGAACAGGATGCATCTTGAAGAGGGATGCAATATGGCTAAGTGGACCGCTAATTATAAAGAGTAAATCGGACGTGAATTGAAGGTCAGAAATAAAATTGTCTGCACATGAGACGAGGGCTGTTTCTGACAGCATCACACCTTTAGACTTACCAGTTGTGCCTGTAGTATACAATATATCAACTATATCTTCTTCAAACTCACATGCTGAAACTTCTGCACTAATGGTATTAAAGTATTCATCTGTAGCTTTCTGCTCCATTGGAACAGCGATGGCACCTATATGGTGCACAGCACAATAAGTTACTACAAAACCTATATCTTGAGTTGAACGAAATACGTATGGCCTGTTAGGTAATACCCCTTCAGACTTAAGTTCTTCTGCCCTCTTAGTTATAGAACTCCATAGCTGAGAGTATGTTATACTATCAGTACCGCAGACTGCAGCTACTTTATCAGGAGTTGCAATTGAATGATGATATATACTTTGCTCTAGTGTCATAGGATGATATTATTCTGAAAGTTTTGACTCAACCATCTTAACGATAGTATCAATTGATCTAAAGTTTCTAGGTGTTACATCAGTAGCATCTAGCGAAATATTGTACTCCTTAGACAAAATTACAAGAATTGTGACTATACCTAAAGAATCCAATTCACTAAAGAGGAAATCAGATTCAAAGTCAACTGCCGGAAGAGCTTCAGACAGGAGTGTTATAATATTCTGTTTCATAGCTTAATTAAATTCAATGTTATTTACAAAATCTGTAGCAGATACTATCGCTATTTCACGTCTATAATCGTCGGGAACTTGAGCAATAATCTTAACCCCAGGATTTAAGTGAGCGAGAAGAATTGCGGATTCCCCGTATCCATTATCAGTATATAAATATTCAGTTTTACCTTTAAGATCGAGCTCAACTATACTTTTAGTATTCGTTTTGAGATTACGTTTTACCGTATTAGTTATAGATATGCCCTTATATAAATAGCGTCCTTTAACAAGTTTGACAGAGTCTTTTGGTATACCAAAAAGTAATGATATAAAGGTAATAGGATATGTTCTATATTTACCGTCCTTCATAGTCAACCACTTAAAAAGAAGAGGTGGGAAAGTGTAAGACATCAGTACAACTGATATCATGCCGACTATTGTCACTTCTGCCAACGAACGCATAGCTGGATGCTTTGATATGATCAATGTACCAATTCCTACAAGCATTATCAAAGCTGATTGAAGGATGCTATTCTTGTATGATGAGAGAATAGGTTTTCTGAATGTGTATTCATGCTGACATCCTTCAGTCATAAAGATTGTATAATCATCTCCCTGAACAAAAATAAAGGTTGCTAGAATTACATTTACAATATTAAACTTTATTCCTACTATAGCCATTATTCCAAGAATCCATACCCAGCTTATTGCCATCGGAATGAATGCAATGATTGCCAATTCAATACGGCCAAAGGAGAACCAGAGAAAGAAGAATACGATGAGTGAACAGGCCCATCCGATATAGTTAAAATTATCAGATAGATTTTTAGAAAGTGCACTATTCATACCTACTACATCGAAACTGTCATCGAAATATGATTTAACAGAATCAATATCACTGGACTCTACAATGAGTTTATTTACTATATATGATTTCCCGGTTTGATCGATTTGAGCAATATTCTGACTAAGAATCAAGCTTGTTAGCGG"""


def mgnify_contig_annotations_response(viral_fragment: ViralFragment) -> str:
    return f"""{viral_fragment.contig_id}	eggNOG-v2	CDS	1058	1597	.	-	.	ID={viral_fragment.contig_id};cog=M;eggnog=Has%20lipid%20A%203-O-deacylase%20activity.%20Hydrolyzes%20the%20ester%20bond%20at%20the%203%20position%20of%20lipid%20A%2C%20a%20bioactive%20component%20of%20lipopolysaccharide%20%28LPS%29%2C%20thereby%20releasing%20the%20primary%20fatty%20acyl%20moiety%20;eggnog_evalue=65.1;eggnog_ortholog=1123037.AUDE01000010_gene2438;eggnog_score=3.8e-08;ogs=NA|NA|NA
{viral_fragment.contig_id}	eggNOG-v2	CDS	1734	2543	.	-	.	ID={viral_fragment.contig_id};brite=ko00000;cog=S;eggnog=Putative%20serine%20esterase%20%28DUF676%29%20;eggnog_evalue=231.9;eggnog_ortholog=1232428.CAVO010000035_gene1395;eggnog_score=3.6e-58;eggnog_tax=aroD;kegg=ko:K06889;ogs=NA|NA|NA;interpro=IPR022742,IPR029058;pfam=PF12146
{viral_fragment.contig_id}	eggNOG-v2	CDS	2554	3879	.	-	.	ID={viral_fragment.contig_id};brite=ko00000,ko01000,ko00001;cog=IQ;ecnumber=6.2.1.41;eggnog=AMP-binding%20enzyme%20C-terminal%20domain%20;eggnog_evalue=445.7;eggnog_ortholog=1122978.AUFP01000001_gene932;eggnog_score=2.6e-122;kegg=ko:K18687;ogs=NA|NA|NA;interpro=IPR000873,IPR042099,IPR025110;pfam=PF13193,PF00501"""


def set_metabolights_project_for_sample(sample: Sample, mtbls: str = "MTBLSDONUT"):
    sample.metabolights_study = mtbls
    sample.save()


@pytest.fixture()
def chicken_mag_catalogue():
    return create_genome_objects()


@pytest.fixture()
def chicken_viral_catalogue():
    return create_viral_objects()


@pytest.fixture(scope="class")
def LiveTests(request):
    class Fixtures:
        pass

    Sample.objects.all().delete()
    GenomeCatalogue.objects.all().delete()
    ViralCatalogue.objects.all().delete()

    Fixtures.animals = [
        Animal.objects.create(
            accession="SAMEG04",
            system=Animal.SALMON,
            animal_code="SSOPHIE",
        )
    ]

    Fixtures.samples = [
        Sample.objects.create(
            accession="SAMEA00000002",
            title="metabolomic extraction",
            animal=Fixtures.animals[0],
            sample_type=Sample.METABOLOMIC,
            metabolights_files=[
                {"file_name": "donut.zip", "sample_name": "SAMEA00000002"}
            ],
        ),
        Sample.objects.create(
            accession="SAMEA00000003",
            title="metagenomic extraction",
            animal=Fixtures.animals[0],
            sample_type=Sample.METAGENOMIC_ASSEMBLY,
        ),
    ]

    set_metabolights_project_for_sample(Fixtures.samples[0])

    Fixtures.genome_catalogues = [create_genome_objects()]
    Fixtures.viral_catalogues = [create_viral_objects()]

    # set a class attribute on the invoking test context
    request.cls.hf_fixtures = Fixtures()

    sample = Fixtures.samples[1]
    marker1 = SampleMetadataMarker.objects.create(
        name="Size of donut", type="DIMENSIONS"
    )
    marker2 = SampleMetadataMarker.objects.create(
        name="Colour of donut", type="COLOURS"
    )
    SampleStructuredDatum.objects.create(
        marker=marker1, sample=sample, measurement="10", units="cm"
    )
    SampleStructuredDatum.objects.create(
        marker=marker2, sample=sample, measurement="Yellow"
    )


@pytest.fixture()
def structured_metadata_marker():
    return SampleMetadataMarker.objects.create(name="Size of donut")


@pytest.fixture()
def salmon_analysis_summary_unpub(salmon_host_sample):
    summary = AnalysisSummary.objects.create(
        title="All about donuts", slug="all-about-donuts", content="# Donuts are a food"
    )
    summary.samples.set([salmon_host_sample])
    return summary
