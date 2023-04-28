import pytest

from holofood.models import (
    SampleStructuredDatum,
    SampleMetadataMarker,
    AnimalStructuredDatum,
    Sample,
)
from holofood.tests.conftest import set_metabolights_project_for_sample


def assert_response_has_n_items(response, n: int):
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == n
    assert data.get("count") == n
    return data


# ------- ANIMAL TESTS -------- #


@pytest.mark.django_db
def test_animals_api_list_empty(client):
    response = client.get("/api/animals")
    assert_response_has_n_items(response, 0)


@pytest.mark.django_db
def test_animals_api_list(
    client, salmon_animal, salmon_metagenomic_sample, salmon_metabolomic_sample
):
    response = client.get("/api/animals")
    data = assert_response_has_n_items(response, 1)

    sample = data.get("items")[0]
    assert sample.get("accession") == salmon_animal.accession
    assert (
        sample.get("canonical_url")
        == f"https://www.ebi.ac.uk/biosamples/{salmon_animal.accession}"
    )

    assert len(sample.get("sample_types")) == 2
    assert salmon_metabolomic_sample.sample_type in sample.get("sample_types")
    assert salmon_metagenomic_sample.sample_type in sample.get("sample_types")
    assert sample.get("system") == "salmon"


@pytest.mark.django_db
def test_animals_api_list_filters(
    client, salmon_animal, chicken_animal, salmon_metagenomic_sample
):
    response = client.get("/api/animals?system=salmon")
    assert_response_has_n_items(response, 1)

    response = client.get("/api/animals?system=chicken")
    assert_response_has_n_items(response, 1)

    response = client.get("/api/animals?require_sample_type=metagenomic_assembly")
    assert_response_has_n_items(response, 1)

    response = client.get("/api/animals?require_sample_type=metabolomic")
    assert_response_has_n_items(response, 0)

    roundness = SampleMetadataMarker.objects.create(name="roundness")
    response = client.get("/api/animals?require_metadata_marker=roundness")
    assert_response_has_n_items(response, 0)

    salmon_roundness = AnimalStructuredDatum.objects.create(
        animal=salmon_animal, marker=roundness, measurement="unknown"
    )
    response = client.get("/api/animals?require_metadata_marker=roundness")
    assert_response_has_n_items(response, 0)

    salmon_roundness.measurement = 3.14
    salmon_roundness.save()

    response = client.get("/api/animals?require_metadata_marker=roundness")
    assert_response_has_n_items(response, 1)


@pytest.mark.django_db
def test_animal_api_detail(
    client, salmon_animal, structured_metadata_marker, salmon_metagenomic_sample
):
    response = client.get("/api/animals/doesnotexist")
    assert response.status_code == 404

    response = client.get(f"/api/animals/{salmon_animal.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("accession") == salmon_animal.accession
    assert data.get("system") == "salmon"
    assert len(data.get("samples")) == 1
    assert (
        data.get("samples")[0].get("accession") == salmon_metagenomic_sample.accession
    )
    assert data.get("sample_types") == [Sample.METAGENOMIC_ASSEMBLY]

    assert len(data.get("structured_metadata")) == 0

    salmon_animal.structured_metadata.create(
        marker=structured_metadata_marker,
        measurement="really quite big",
        units="cm",
        source=AnimalStructuredDatum.BIOSAMPLES,
    )

    response = client.get(f"/api/animals/{salmon_animal.accession}")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("structured_metadata")) == 1
    assert data.get("structured_metadata")[0].get("measurement") == "really quite big"


@pytest.mark.django_db
def test_animals_export(client, salmon_animal):
    response = client.get("/export/animals")
    assert response.status_code == 200
    data = response.content.decode()
    assert "accession" in data
    assert salmon_animal.accession in data


@pytest.mark.django_db
def test_animal_metadata_export(client, salmon_animal, structured_metadata_marker):
    salmon_animal.structured_metadata.create(
        marker=structured_metadata_marker,
        measurement="really quite big",
        units="cm",
        source=AnimalStructuredDatum.BIOSAMPLES,
    )
    response = client.get(f"/export/animals/{salmon_animal.accession}/metadata")
    assert response.status_code == 200
    data = response.content.decode()
    assert "marker" in data
    assert "really quite big" in data


# ------- SAMPLE TESTS -------- #


@pytest.mark.django_db
def test_samples_api_list_empty(client):
    response = client.get("/api/samples")
    assert_response_has_n_items(response, 0)


@pytest.mark.django_db
def test_samples_api_list(client, salmon_metagenomic_sample):
    response = client.get("/api/samples")
    data = assert_response_has_n_items(response, 1)

    sample = data.get("items")[0]
    assert sample.get("accession") == salmon_metagenomic_sample.accession
    assert sample.get("title") == salmon_metagenomic_sample.title
    assert sample.get("sample_type") == salmon_metagenomic_sample.METAGENOMIC_ASSEMBLY
    assert (
        sample.get("canonical_url")
        == f"https://www.ebi.ac.uk/ena/browser/view/{salmon_metagenomic_sample.accession}"
    )


@pytest.mark.django_db
def test_samples_api_list_filters(client, salmon_metagenomic_sample):
    response = client.get("/api/samples?system=salmon")
    assert_response_has_n_items(response, 1)

    response = client.get("/api/samples?system=chicken")
    assert_response_has_n_items(response, 0)

    response = client.get("/api/samples?title=doughnut")
    assert_response_has_n_items(response, 0)

    response = client.get("/api/samples?title=donut")
    assert_response_has_n_items(response, 1)

    response = client.get("/api/samples?animal_accession=freddiefrog")
    assert_response_has_n_items(response, 0)

    response = client.get(
        f"/api/samples?animal_accession={salmon_metagenomic_sample.animal.accession}"
    )
    assert_response_has_n_items(response, 1)

    response = client.get("/api/samples?require_metadata_marker=roundness")
    assert_response_has_n_items(response, 0)

    roundness = SampleMetadataMarker.objects.create(name="roundness")
    response = client.get("/api/samples?require_metadata_marker=roundness")
    assert_response_has_n_items(response, 0)

    salmon_roundness = SampleStructuredDatum.objects.create(
        sample=salmon_metagenomic_sample, marker=roundness, measurement="unknown"
    )
    response = client.get("/api/samples?require_metadata_marker=roundness")
    assert_response_has_n_items(response, 0)

    salmon_roundness.measurement = 3.14
    salmon_roundness.save()

    response = client.get("/api/samples?require_metadata_marker=roundness")
    assert_response_has_n_items(response, 1)


@pytest.mark.django_db
def test_samples_api_detail(
    client, salmon_metagenomic_sample, structured_metadata_marker
):
    response = client.get("/api/samples/doesnotexist")
    assert response.status_code == 404

    response = client.get(f"/api/samples/{salmon_metagenomic_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("accession") == salmon_metagenomic_sample.accession
    assert data.get("title") == salmon_metagenomic_sample.title
    assert data.get("animal") == salmon_metagenomic_sample.animal.accession
    assert data.get("sample_type") == Sample.METAGENOMIC_ASSEMBLY
    assert (
        data.get("metagenomics_url")
        == f"https://www.ebi.ac.uk/metagenomics/api/v1/samples/{salmon_metagenomic_sample.accession}"
    )
    assert data.get("metabolomics_url") == None

    assert len(data.get("structured_metadata")) == 0

    salmon_metagenomic_sample.structured_metadata.create(
        marker=structured_metadata_marker,
        measurement="really quite big",
        units="cm",
        source=SampleStructuredDatum.BIOSAMPLES,
    )

    response = client.get(f"/api/samples/{salmon_metagenomic_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("structured_metadata")) == 1
    assert data.get("structured_metadata")[0].get("measurement") == "really quite big"


@pytest.mark.django_db
def test_sample_metadata_markers_api_list_filters(
    client, salmon_animal, salmon_metabolomic_sample, structured_metadata_marker
):
    response = client.get("/api/sample_metadata_markers")
    assert_response_has_n_items(response, 1)

    response = client.get("/api/sample_metadata_markers?name=donut")
    assert_response_has_n_items(response, 1)

    response = client.get("/api/sample_metadata_markers?name=donut&min_samples=2")
    assert_response_has_n_items(response, 0)

    response = client.get("/api/sample_metadata_markers?name=cronut")
    assert_response_has_n_items(response, 0)

    AnimalStructuredDatum.objects.create(
        animal=salmon_animal, marker=structured_metadata_marker, measurement="2"
    )
    SampleStructuredDatum.objects.create(
        sample=salmon_metabolomic_sample,
        marker=structured_metadata_marker,
        measurement="3",
    )
    response = client.get("/api/sample_metadata_markers?min_samples=2")
    assert_response_has_n_items(response, 0)
    response = client.get("/api/sample_metadata_markers?min_animals=2")
    assert_response_has_n_items(response, 0)
    response = client.get("/api/sample_metadata_markers?min_samples=1")
    assert_response_has_n_items(response, 1)
    response = client.get("/api/sample_metadata_markers?min_animals=1")
    assert_response_has_n_items(response, 1)


@pytest.mark.django_db
def test_metagenomics(client, salmon_metagenomic_sample):
    response = client.get(f"/api/samples/{salmon_metagenomic_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("sample_type") == Sample.METAGENOMIC_ASSEMBLY
    assert "ena" in data.get("canonical_url").lower()
    assert (
        data.get("metagenomics_url")
        == f"https://www.ebi.ac.uk/metagenomics/api/v1/samples/{salmon_metagenomic_sample.accession}"
    )


@pytest.mark.django_db
def test_metabolomics(client, salmon_metabolomic_sample):
    response = client.get(f"/api/samples/{salmon_metabolomic_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("sample_type") == Sample.METABOLOMIC
    assert "biosamples" in data.get("canonical_url").lower()
    assert data.get("metabolomics_url") == None

    set_metabolights_project_for_sample(salmon_metabolomic_sample)

    response = client.get(f"/api/samples/{salmon_metabolomic_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("sample_type") == Sample.METABOLOMIC
    assert data.get("metabolomics_url").endswith(
        f"ebi.ac.uk/metabolights/ws/studies/MTBLSDONUT"
    )


@pytest.mark.django_db
def test_non_processed_samples(client, salmon_histological_sample, salmon_host_sample):
    response = client.get(f"/api/samples/{salmon_histological_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("sample_type") == Sample.HISTOLOGICAL
    assert "biosamples" in data.get("canonical_url").lower()

    response = client.get(f"/api/samples/{salmon_host_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("sample_type") == Sample.HOST_GENOMIC
    assert "ena" in data.get("canonical_url").lower()


@pytest.mark.django_db
def test_samples_export(client, salmon_host_sample):
    response = client.get("/export/samples")
    assert response.status_code == 200
    data = response.content.decode()
    assert "accession" in data
    assert salmon_host_sample.accession in data


@pytest.mark.django_db
def test_sample_metadata_export(client, salmon_host_sample, structured_metadata_marker):
    salmon_host_sample.structured_metadata.create(
        marker=structured_metadata_marker,
        measurement="really quite big",
        units="cm",
        source=AnimalStructuredDatum.BIOSAMPLES,
    )
    response = client.get(f"/export/samples/{salmon_host_sample.accession}/metadata")
    assert response.status_code == 200
    data = response.content.decode()
    assert "marker" in data
    assert "really quite big" in data


# ------- ANALYSIS SUMMARY TESTS -------- #


@pytest.mark.django_db
def test_analysis_summaries_list(
    client, salmon_host_sample, salmon_analysis_summary_unpub
):
    response = client.get("/api/analysis-summaries")
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 0
    assert len(data.get("items")) == 0

    salmon_analysis_summary_unpub.is_published = True
    salmon_analysis_summary_unpub.save()
    response = client.get("/api/analysis-summaries")
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 1
    assert len(data.get("items")) == 1
    assert data.get("items")[0].get("title") == "All about donuts"


@pytest.mark.django_db
def test_mag_catalogues(client, chicken_mag_catalogue):
    response = client.get("/api/genome-catalogues")
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 1
    assert data.get("items")[0]["id"] == chicken_mag_catalogue.id

    response = client.get(f"/api/genome-catalogues/{chicken_mag_catalogue.id}")
    assert response.status_code == 200
    data = response.json()
    assert all(
        [
            key in data
            for key in ["id", "title", "biome", "related_mag_catalogue_id", "system"]
        ]
    )
    assert data.get("system") == "chicken"

    response = client.get(f"/api/genome-catalogues/{chicken_mag_catalogue.id}/genomes")
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 1
    assert (
        data.get("items")[0]["accession"]
        == chicken_mag_catalogue.genomes.first().accession
    )


@pytest.mark.django_db
def test_mag_catalogues_export(client, chicken_mag_catalogue):
    response = client.get(
        f"/export/genome-catalogues/{chicken_mag_catalogue.id}/genomes"
    )
    assert response.status_code == 200
    data = response.content.decode()
    assert "accession" in data
    assert chicken_mag_catalogue.genomes.first().accession in data


@pytest.mark.django_db
def test_viral_catalogues(client, chicken_viral_catalogue):
    response = client.get("/api/viral-catalogues")
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 1
    assert data.get("items")[0]["id"] == chicken_viral_catalogue.id

    response = client.get(f"/api/viral-catalogues/{chicken_viral_catalogue.id}")
    assert response.status_code == 200
    data = response.json()
    assert all(
        [
            key in data
            for key in [
                "id",
                "title",
                "biome",
                "related_genome_catalogue_url",
                "related_genome_catalogue",
                "system",
            ]
        ]
    )
    assert data.get("system") == "chicken"
    assert (
        data.get("related_genome_catalogue", {}).get("id")
        == chicken_viral_catalogue.related_genome_catalogue.id
    )

    response = client.get(
        f"/api/viral-catalogues/{chicken_viral_catalogue.id}/fragments"
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 2
    assert (
        data.get("items")[0]["id"] == chicken_viral_catalogue.viral_fragments.first().id
    )


@pytest.mark.django_db
def test_viral_catalogues_export(client, chicken_viral_catalogue):
    response = client.get(
        f"/export/viral-catalogues/{chicken_viral_catalogue.id}/fragments"
    )
    assert response.status_code == 200
    data = response.content.decode()
    assert "id" in data
    assert chicken_viral_catalogue.viral_fragments.first().id in data
