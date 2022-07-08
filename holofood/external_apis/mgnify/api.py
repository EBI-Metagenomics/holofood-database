import logging

import requests

from holofood.utils import holofood_config, clean_keys

API_ROOT = holofood_config.mgnify.api_root.rstrip("/")


def assert_response_is_acceptable(response):
    try:
        assert response.status_code in (requests.codes.ok, requests.codes.not_found)
    except AssertionError:
        raise Exception(
            f"Response from MGnify API for {response.request.url} was neither 200 (Okay) or 404 (Not found). "
            f"Instead, {response.status_code}"
        )


def get_metagenomics_existence_for_sample(sample: str) -> bool:
    logging.info(f"Fetching {sample} metagenomics data from MGnify {API_ROOT = }")

    response = requests.get(f"{API_ROOT}/samples/{sample}")
    assert_response_is_acceptable(response)
    return response.status_code == requests.codes.ok


def get_metagenomics_analyses_for_run(run: str) -> list[dict]:
    logging.info(f"Fetching analyses for {run = } from MGnify {API_ROOT = }")

    response = requests.get(f"{API_ROOT}/runs/{run}/analyses?page_size=50")
    assert_response_is_acceptable(response)

    return clean_keys(response.json()).get("data", [])
