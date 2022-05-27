import logging
from json import JSONDecodeError

import requests

from holofood.utils import holofood_config

API_ROOT = holofood_config.biosamples.api_root.rstrip("/")


def get_sample_structured_data(sample: str) -> dict:
    logging.info(f"Fetching {sample} structured data from Biosamples {API_ROOT = }")

    response = requests.get(f"{API_ROOT}/structureddata/{sample}")
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
