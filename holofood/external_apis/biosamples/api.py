import logging
from json import JSONDecodeError
from typing import List

import requests

from holofood.utils import holofood_config

API_ROOT = holofood_config.biosamples.api_root.rstrip("/")


def get_sample_structured_data(sample: str) -> List[dict]:
    logging.info(f"Fetching {sample} structured data from Biosamples {API_ROOT = }")

    response = requests.get(f"{API_ROOT}/structureddata/{sample}")
    if response.status_code == requests.codes.not_found:
        logging.info(f"No structureddata for sample {sample}")
        return []
    try:
        data = response.json()
    except (JSONDecodeError, KeyError, AttributeError) as e:
        logging.error("Could not read structureddata from biosamples")
        raise e

    try:
        sample_data = next(
            data_section
            for data_section in data.get("data", [])
            if data_section.get("type") == "SAMPLE"
        )
    except StopIteration:
        logging.warning(f"No structureddata for sample {sample}")
        return []
    return sample_data.get("content")
