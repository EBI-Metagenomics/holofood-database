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
    username: str = ""
    password: str = ""
    auth_url: AnyHttpUrl = "https://www.ebi.ac.uk/ena/submit/webin/auth/token"


class EnaConfig(BaseModel):
    systems: dict = {}
    username: str = ""
    password: str = ""
    portal_api_root: AnyHttpUrl = "https://www.ebi.ac.uk/ena/portal/api"
    browser_api_root: AnyHttpUrl = "https://www.ebi.ac.uk/ena/browser/api"
    browser_url: AnyHttpUrl = "https://www.ebi.ac.uk/ena/browser/view"


class MgnifyConfig(BaseModel):
    api_root: AnyHttpUrl = "https://www.ebi.ac.uk/metagenomics/api/v1"
    web_url: AnyHttpUrl = "https://www.ebi.ac.uk/metagenomics"
    request_cadence: timedelta = timedelta(seconds=3)
    request_timeout: timedelta = timedelta(seconds=15.05)
    request_retries: int = 3


class MetabolightsConfig(BaseModel):
    api_root: AnyHttpUrl = "https://www.ebi.ac.uk/metabolights/ws"
    web_url: AnyHttpUrl = "https://www.ebi.ac.uk/metabolights"
    user_token: str = None
    biosample_column_name_in_sample_table: str = "Characteristics[BioSamples accession]"


class SampleTableConfig(BaseModel):
    default_metadata_marker_columns: List[str]


class MetadataTableConfig(BaseModel):
    bring_to_top_if_metadata_marker_name_contains: List[str]


class TablesConfig(BaseModel):
    animals_list: SampleTableConfig = []
    metadata_list: MetadataTableConfig = []


class DocsConfig(BaseModel):
    docs_url: AnyHttpUrl = "https://docs.holofooddata.org"
    portal_doi: str = "10.5281/zenodo.7684072"


class PortalConfig(BaseModel):
    url_root: AnyHttpUrl = "https://www.holofooddata.org"


class HolofoodConfig(BaseSettings):
    mock_apis: bool = False

    biosamples: BiosamplesConfig = BiosamplesConfig()
    ena: EnaConfig = EnaConfig()
    mgnify: MgnifyConfig = MgnifyConfig()
    docs: DocsConfig = DocsConfig()
    metabolights: MetabolightsConfig = MetabolightsConfig()
    tables: TablesConfig = TablesConfig()
    portal: PortalConfig = PortalConfig()

    class Config:
        env_prefix = "holofood_"
        env_nested_delimiter = "__"
        # E.g. set the env var `HOLOFOOD_BIOSAMPLES__API_ROOT` to override the default

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
