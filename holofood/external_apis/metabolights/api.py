import csv
import logging
from contextlib import closing
from json import JSONDecodeError
from typing import List

import requests

from holofood.external_apis.metabolights.auth import MTBLS_AUTH
from holofood.utils import holofood_config

API_ROOT = holofood_config.metabolights.api_root.rstrip("/")


def _parse_metabolights_response(response, as_json=True):
    if response.status_code in (requests.codes.not_found, requests.codes.forbidden):
        logging.info(f"No metabolights info found for {response.url}")
        return {}

    if response.status_code == requests.codes.not_acceptable:
        logging.warning(f"Metabolights said {response.url} was an unacceptable request")
        return {}

    if as_json:
        try:
            data = response.json()
        except (JSONDecodeError, KeyError, AttributeError) as e:
            logging.error(f"Could not read metabolights response for {response.url}")
            raise e
        return data
    return response.text


def get_metabolights_assays(mtbls_accession: str, sample_accession: str) -> List[dict]:
    logging.info(
        f"Fetching metabolights details for {mtbls_accession} {sample_accession}"
    )

    samples_metadata_filename = None
    response = requests.get(
        f"{API_ROOT}/studies/{mtbls_accession}/files?include_raw_data=false",
        auth=MTBLS_AUTH,
    )
    data = _parse_metabolights_response(response)
    metadata_files = data.get("study", [])
    for file in metadata_files:
        if file.get("type") == "metadata_sample":
            samples_metadata_filename = file.get("file")

    if not samples_metadata_filename:
        logging.warning(f"Did not find sample metadata sheet for {mtbls_accession}")
        return []

    sample_name = None
    with closing(
        requests.get(
            f"{API_ROOT}/studies/{mtbls_accession}/download?file={samples_metadata_filename}",
            stream=True,
        )
    ) as stream:
        reader = csv.DictReader(stream.iter_lines(), delimiter="\t")
        for row in reader:
            print(row)
            if (
                row.get(
                    holofood_config.metabolights.biosample_column_name_in_sample_table
                )
                == sample_accession
            ):
                sample_name = row.get("Sample Name")
                break

    if not sample_name:
        logging.warning(
            f"Did not find biosample {sample_accession} in sample metadata sheet"
        )
        return []

    assay_sheets = [
        file.get("file")
        for file in metadata_files
        if file.get("type") == "metadata_assay"
    ]

    assay_sheet_rows_for_sample = []
    for assay_sheet in assay_sheets:
        with closing(
            requests.get(
                f"{API_ROOT}/studies/{mtbls_accession}/download?file={assay_sheet}",
                stream=True,
            )
        ) as stream:
            reader = csv.DictReader(stream.iter_lines(), "utf-8", delimiter="\t")
            for row in reader:
                print(row)
                if row.get("Sample Name") == sample_name:
                    assay_sheet_rows_for_sample.append(row)

    return assay_sheet_rows_for_sample
