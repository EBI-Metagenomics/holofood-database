import logging
from json import JSONDecodeError
from typing import List

import requests

from holofood.utils import holofood_config

API_ROOT = holofood_config.biosamples.api_root.rstrip("/")


def get_auth_headers():
    if holofood_config.biosamples.username:
        auth_data = {
            "authRealms": ["ENA"],
            "username": holofood_config.biosamples.username,
            "password": holofood_config.biosamples.password,
        }
        token_response = requests.post(
            f"{holofood_config.biosamples.auth_url}", json=auth_data
        )
        if not token_response.status_code == 200:
            logging.error(token_response.text)
            raise Exception("Could not get token for BioSamples API")
        return {"Authorization": f"Bearer {token_response.text}"}
    return {}


def get_sample_structured_data(sample: str) -> dict:
    auth_headers = get_auth_headers()
    if auth_headers:
        logging.info("Using authenticated BioSamples API")

    logging.info(f"Fetching {sample} structured data from Biosamples {API_ROOT = }")

    response = requests.get(f"{API_ROOT}/structureddata/{sample}", headers=auth_headers)
    if response.status_code == requests.codes.not_found:
        logging.info(f"No structureddata for sample {sample}")
        return {}
    try:
        data = response.json()
    except (JSONDecodeError, KeyError, AttributeError) as e:
        logging.error("Could not read structureddata from biosamples")
        raise e

    return {
        data_section.get("type"): data_section.get("content", [])
        for data_section in data.get("data", [])
    }


def get_biosample(sample: str) -> dict:
    auth_headers = get_auth_headers()
    if auth_headers:
        logging.info("Using authenticated BioSamples API")

    logging.info(f"Fetching {sample} from Biosamples {API_ROOT = }")

    response = requests.get(f"{API_ROOT}/samples/{sample}", headers=auth_headers)
    if response.status_code == requests.codes.not_found:
        logging.info(f"No biosample for sample {sample}")
        return {}
    try:
        data = response.json()
    except (JSONDecodeError, KeyError, AttributeError) as e:
        logging.error("Could not read response from biosamples")
        raise e
    return data


def get_project_samples(
    project_attr: str,
    webin_filter: List[str],
    max_pages: int = None,
    begin_at_cursor: str = None,
    updated_since: str = None,
) -> List[dict]:
    """
    Generator for pages of biosamples for a specific project. Each page is up to 200 biosamples.

    :param updated_since: ISO8601 formatted date string to filter for samples updated since
    :param begin_at_cursor: Starting cursor value for pagination
    :param project_attr: e.g. HoloFood - the biosamples search value for attr:project:<value>
    :param webin_filter: list of webin IDs to limit results to. Discards samples from other submitters.
    :param max_pages: Max number of pages to yield.
    :return: List of dicts, each representing the JSON for a biosample.
    """
    auth_headers = get_auth_headers()
    if auth_headers:
        logging.info("Using authenticated BioSamples API")
        logging.info(auth_headers)

    logging.info(
        f"Fetching samples from Biosamples {API_ROOT = } for {project_attr = }"
    )

    next_url = f"{API_ROOT}/samples?filter=attr:project:{project_attr.strip()}&size=200"
    if updated_since:
        next_url = f"{next_url}&filter=dt:update:from={updated_since}"
    if begin_at_cursor:
        next_url = f"{next_url}&cursor={begin_at_cursor}"
    pages = 0

    while next_url is not None:
        response = requests.get(next_url, headers=auth_headers)
        logging.info(f"Fetching samples page from Biosamples {next_url}")
        try:
            data = response.json()
        except (JSONDecodeError, KeyError, AttributeError) as e:
            logging.error("Could not read samples from biosamples")
            raise e
        try:
            next_url = data["_links"].get("next", {}).get("href")
        except KeyError as e:
            logging.error("Could not find URL for next page of data")
            raise e
        else:
            pages += 1
            if max_pages and pages >= max_pages:
                logging.warning(f"Truncating biosamples pagination after {pages} pages")
                next_url = None

        samples = data.get("_embedded", {}).get("samples", [])
        for sample in samples:
            if sample.get("webinSubmissionAccountId") in webin_filter:
                yield sample
