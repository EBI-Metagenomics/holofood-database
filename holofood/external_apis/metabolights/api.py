import logging
from itertools import groupby
from json import JSONDecodeError

import requests

from holofood.external_apis.metabolights.auth import MTBLS_AUTH
from holofood.utils import holofood_config

API_ROOT = holofood_config.metabolights.api_root.rstrip("/")


def get_metabolights_project_files(mtbls_project_accession: str) -> dict:
    logging.info(f"Fetching metabolights project files for {mtbls_project_accession}")
    response = requests.get(
        f"{API_ROOT}/studies/{mtbls_project_accession}/files/samples", auth=MTBLS_AUTH
    )

    if response.status_code in (requests.codes.not_found, requests.codes.forbidden):
        logging.info(f"No metabolights samples for projects {mtbls_project_accession}")
        return {}

    if response.status_code == requests.codes.not_acceptable:
        logging.warning(
            f"Metabolights said {mtbls_project_accession} was a bad accession"
        )
        return {}

    try:
        data = response.json()
    except (JSONDecodeError, KeyError, AttributeError) as e:
        logging.error(
            f"Could not read metabolights samples files for {mtbls_project_accession}"
        )
        raise e
    logging.warning(response.status_code)

    by_sample_name = lambda file: file.get("sample_name")
    files_per_sample = groupby(
        sorted(data.get("sample_files"), key=by_sample_name), key=by_sample_name
    )
    return {sample: list(files) for sample, files in files_per_sample}
