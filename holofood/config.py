"""

   Copyright EMBL-European Bioinformatics Institute, 2022

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
from __future__ import annotations
from datetime import timedelta
import json
from pathlib import Path
from typing import Any, List

from pydantic import BaseSettings, AnyHttpUrl, BaseModel


def data_config_source(settings: BaseSettings) -> dict[str, Any]:
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path("config/data_config.json").read_text(encoding))


class BiosamplesConfig(BaseModel):
    api_root: AnyHttpUrl = "https://www.ebi.ac.uk/biosamples"
    project_id: str = "HF"


class EnaConfig(BaseModel):
    projects: List[str] = []
    systems: dict = {}
    username: str = "Webin-0"
    password: str = "secret"
    portal_api_root: AnyHttpUrl = "https://www.ebi.ac.uk/ena/portal/api"
    browser_url: AnyHttpUrl = "https://www.ebi.ac.uk/ena/browser/view"
    submit_api_root: AnyHttpUrl = "https://www.ebi.ac.uk/ena/submit"


class MgnifyConfig(BaseModel):
    api_root: AnyHttpUrl = "https://www.ebi.ac.uk/metagenomics/api/v1"
    web_url: AnyHttpUrl = "https://www.ebi.ac.uk/metagenomics"
    request_cadence: timedelta = timedelta(seconds=3)


class MetabolightsConfig(BaseModel):
    web_url: AnyHttpUrl = "https://www.ebi.ac.uk/metabolights"


class SampleTableConfig(BaseModel):
    default_metadata_marker_columns: List[str]


class TablesConfig(BaseModel):
    samples_list: SampleTableConfig = []


class HolofoodConfig(BaseSettings):
    mock_apis: bool = False

    biosamples: BiosamplesConfig = BiosamplesConfig()
    ena: EnaConfig = EnaConfig()
    mgnify: MgnifyConfig = MgnifyConfig()
    metabolights: MetabolightsConfig = MetabolightsConfig()
    tables: TablesConfig = TablesConfig()

    class Config:
        env_prefix = "holofood_"
        env_nested_delimiter = "__"
        # E.g. set the env var `HOLOFOOD_ENA__PROJECTS` to override the default

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                data_config_source,
                env_settings,
                file_secret_settings,
            )
