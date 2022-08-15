from __future__ import annotations

import logging
from json import JSONDecodeError
from typing import List

import requests
from django.conf import settings

from holofood.external_apis.ena.auth import ENA_AUTH
from holofood.utils import holofood_config

API_ROOT = holofood_config.ena.portal_api_root.rstrip("/")


def get_holofood_readruns(
    project_ids=settings.HOLOFOOD_CONFIG.ena.projects,
) -> dict[List[dict]]:
    logging.info(f"Fetching reads/samples from ENA {API_ROOT = }")
    logging.info(project_ids)
    assert project_ids is not None

    ena_projects_runs = {}
    for project in project_ids:
        response = requests.get(
            f"{API_ROOT}/search?format=json&dataPortal=ena&result=read_run&query=study_accession={project}&fields=sample_accession,project_name,sample_title,checklist",
            auth=ENA_AUTH,
        )
        try:
            reads_list = response.json()
        except JSONDecodeError:
            logging.warning(f"No response for ENA Project {project}")
            continue
        if type(reads_list) is not list:
            logging.warning(f"Bad read_runs list received for ENA Project {project}")
            continue
        ena_projects_runs[project] = reads_list

    return ena_projects_runs
