import logging
from typing import List

import requests
from requests.adapters import HTTPAdapter

from holofood.utils import holofood_config, clean_keys, CadenceEnforcer


class MgnifyApi:
    def __init__(self):
        self.session = requests.Session()
        self.api_root = holofood_config.mgnify.api_root.rstrip("/")
        self.session.mount(
            self.api_root,
            HTTPAdapter(max_retries=holofood_config.mgnify.request_retries),
        )
        self.request_options = {
            "timeout": holofood_config.mgnify.request_timeout.total_seconds(),
        }
        self._request_slower = CadenceEnforcer(
            min_period=holofood_config.mgnify.request_cadence
        )

    def get(self, endpoint):
        return self.session.get(
            f'{self.api_root}/{endpoint.lstrip("/")}', **self.request_options
        )

    def __str__(self):
        return f"MGnify API @ {self.api_root}"

    @staticmethod
    def assert_response_is_acceptable(response):
        if response.status_code not in (requests.codes.ok, requests.codes.not_found):
            raise Exception(
                f"Response from MGnify API for {response.request.url} was neither 200 (Okay) or 404 (Not found). "
                f"Instead, {response.status_code}"
            )

    def get_metagenomics_existence_for_sample(self, sample: str) -> bool:
        logging.info(f"Fetching {sample} metagenomics data from {self}")

        self._request_slower()
        response = self.get(
            f"samples/{sample}",
        )
        self.assert_response_is_acceptable(response)
        return response.status_code == requests.codes.ok

    def get_metagenomics_samples_for_project(self, project: str) -> List[str]:
        logging.info(f"Fetching {project} metagenomics data from {self}")
        page = 1
        samples = []
        while page:
            self._request_slower()
            response = self.get(f"/studies/{project}/samples?{page=}")
            self.assert_response_is_acceptable(response)
            if response.status_code == requests.codes.not_found:
                return samples
            data = response.json()
            samples.extend(
                map(lambda sample: sample["attributes"]["biosample"], data["data"])
            )

            has_more_pages = data["links"]["next"] is not None
            if has_more_pages:
                page += 1
            else:
                page = None
        return samples

    def get_metagenomics_analyses_for_run(self, run: str) -> List[dict]:
        logging.info(f"Fetching analyses for {run = } from {self}")

        self._request_slower()
        response = self.get(f"runs/{run}/analyses?page_size=50")
        self.assert_response_is_acceptable(response)

        return clean_keys(response.json()).get("data", [])
