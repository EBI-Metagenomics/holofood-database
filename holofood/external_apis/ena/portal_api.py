from __future__ import annotations

import logging
from json import JSONDecodeError
from typing import Optional

import requests

from holofood.external_apis.ena.auth import ENA_AUTH
from holofood.utils import holofood_config

API_ROOT = holofood_config.ena.portal_api_root.rstrip("/")


def get_filereport(sample_accession: str) -> Optional[dict]:
    logging.info(f"Fetching sample filereport from ENA {API_ROOT = }")
    if ENA_AUTH:
        logging.info("Using authenticated ENA Portal API")
    response = requests.get(
        f"{API_ROOT}/filereport?result=read_run&accession={sample_accession}&format=json&"
        f"fields=sample_title,experiment_accession,experiment_title,study_accession,study_title,"
        f"run_accession,run_alias,read_count,base_count",
        auth=ENA_AUTH,
    )
    try:
        related_records = response.json()[0]
    except (JSONDecodeError, KeyError):
        logging.warning(f"No ENA filereport response for {sample_accession}")
        return None
    return related_records
