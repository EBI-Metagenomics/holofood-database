import pytest

from holofood.models import SampleStructuredDatum


@pytest.mark.django_db
def test_samples_api_list_empty(client):
    response = client.get("/api/samples")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 0
    assert data.get("count") == 0


@pytest.mark.django_db
def test_samples_api_list(client, salmon_sample):
    response = client.get("/api/samples")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 1
    assert data.get("count") == 1

    sample = data.get("items")[0]
    assert sample.get("accession") == salmon_sample.accession
    assert sample.get("title") == salmon_sample.title
    assert (
        sample.get("canonical_url")
        == f"https://www.ebi.ac.uk/ena/browser/view/{salmon_sample.accession}"
    )
    assert sample.get("project").get("accession") == salmon_sample.project.accession
    assert sample.get("project").get("title") == salmon_sample.project.title
    assert (
        sample.get("project").get("canonical_url")
        == f"https://www.ebi.ac.uk/ena/browser/view/{salmon_sample.project.accession}"
    )
    assert sample.get("system") == "salmon"


@pytest.mark.django_db
def test_samples_api_list_filters(client, salmon_sample):
    response = client.get("/api/samples?system=salmon")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 1
    assert data.get("count") == 1

    response = client.get("/api/samples?system=chicken")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 0
    assert data.get("count") == 0

    response = client.get("/api/samples?title=doughnut")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 0
    assert data.get("count") == 0

    response = client.get("/api/samples?title=donut")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 1
    assert data.get("count") == 1

    response = client.get("/api/samples?project_title=doughnut")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 0
    assert data.get("count") == 0

    response = client.get("/api/samples?project_title=donut")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("items")) == 1
    assert data.get("count") == 1


@pytest.mark.django_db
def test_samples_api_detail(client, salmon_sample, structured_metadata_marker):
    response = client.get("/api/samples/doesnotexist")
    assert response.status_code == 404

    response = client.get(f"/api/samples/{salmon_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("accession") == salmon_sample.accession
    assert data.get("title") == salmon_sample.title
    assert data.get("project").get("accession") == salmon_sample.project.accession
    assert data.get("project").get("title") == salmon_sample.project.title
    assert data.get("system") == "salmon"
    assert len(data.get("structured_metadata")) == 0

    salmon_sample.structured_metadata.create(
        marker=structured_metadata_marker,
        measurement="really quite big",
        units="cm",
        source=SampleStructuredDatum.BIOSAMPLES,
    )

    response = client.get(f"/api/samples/{salmon_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("structured_metadata")) == 1
    assert data.get("structured_metadata")[0].get("measurement") == "really quite big"


@pytest.mark.django_db
def test_metagenomics(client, salmon_sample):
    response = client.get(f"/api/samples/{salmon_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert not data.get("has_metagenomics")
    assert data.get("metagenomics_url") is None

    salmon_sample.has_metagenomics = True
    salmon_sample.save()
    response = client.get(f"/api/samples/{salmon_sample.accession}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("has_metagenomics")
    assert (
        data.get("metagenomics_url")
        == f"https://www.ebi.ac.uk/metagenomics/api/v1/samples/{salmon_sample.accession}"
    )


@pytest.mark.django_db
def test_annotations_list(client, salmon_sample, salmon_annotation_unpub):
    response = client.get("/api/annotations")
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 0
    assert len(data.get("items")) == 0

    salmon_annotation_unpub.is_published = True
    salmon_annotation_unpub.save()
    response = client.get("/api/annotations")
    assert response.status_code == 200
    data = response.json()
    assert data.get("count") == 1
    assert len(data.get("items")) == 1
    assert data.get("items")[0].get("title") == "All about donuts"


@pytest.mark.django_db
def test_annotations_export(client, salmon_sample):
    response = client.get("/export/samples")
    assert response.status_code == 200
    data = response.content.decode()
    assert "accession" in data
    assert salmon_sample.accession in data


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
    response = client.get(f"/api/genome-catalogues/{chicken_mag_catalogue.id}/genomes")
    assert response.status_code == 200
    data = response.content.decode()
    assert "accession" in data
    assert chicken_mag_catalogue.genomes.first().accession in data
