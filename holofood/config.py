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
import json
from typing import List

from pydantic import BaseSettings, AnyHttpUrl, BaseModel, validator


class BiosamplesConfig(BaseModel):
    api_root: AnyHttpUrl = "http://example.com/biosamples"
    project_id: str = "HF"


class EnaConfig(BaseModel):
    @validator("projects", pre=True)
    def projects_is_list(cls, v):
        try:
            projects = json.loads(v)
        except json.JSONDecodeError:
            raise ValueError("value is not valid json")
        return projects

    projects: List[str] = []
    username: str = "Webin-0"
    password: str = "secret"
    portal_api_root: AnyHttpUrl = "https://www.ebi.ac.uk/ena/portal/api"
    browser_url: AnyHttpUrl = "https://www.ebi.ac.uk/ena/browser/view"
    submit_api_root: AnyHttpUrl = "https://www.ebi.ac.uk/ena/submit"


class HolofoodConfig(BaseSettings):
    mock_apis: bool = False

    biosamples: BiosamplesConfig = BiosamplesConfig()
    ena: EnaConfig = EnaConfig()

    class Config:
        env_prefix = "holofood_"
        env_nested_delimiter = "__"
        # E.g. set the env var `HOLOFOOD_ENA__PROJECTS` to override the default
