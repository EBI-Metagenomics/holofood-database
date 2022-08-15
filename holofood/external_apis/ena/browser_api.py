import logging
from dataclasses import dataclass, field
from typing import Optional, List

import requests
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers import XmlParser

from holofood.external_apis.ena.auth import ENA_AUTH
from holofood.utils import holofood_config

API_ROOT = holofood_config.ena.browser_api_root.rstrip("/")


@dataclass
class SampleAttribute:

    tag: str = field(metadata={"name": "TAG"})
    value: str = field(metadata={"name": "VALUE"})
    units: Optional[str] = field(default=None, metadata={"name": "UNITS"})


@dataclass
class SampleAttributeSet:
    class Meta:
        name = "SAMPLE_ATTRIBUTES"

    values: List[SampleAttribute] = field(
        default_factory=list, metadata={"name": "SAMPLE_ATTRIBUTE"}
    )


@dataclass
class SampleMetadata:
    class Meta:
        name = "SAMPLE"

    accession: str = field(metadata={"type": "Attribute", "name": "accession"})
    alias: str = field(metadata={"type": "Attribute", "name": "alias"})

    title: str = field(metadata={"name": "TITLE"})
    attributes: SampleAttributeSet = field(metadata={"name": "SAMPLE_ATTRIBUTES"})

    centre_name: Optional[str] = field(
        default=None, metadata={"type": "Attribute", "name": "centre_name"}
    )


@dataclass
class SampleMetadataSet:
    class Meta:
        name = "SAMPLE_SET"

    samples: List[SampleMetadata] = field(
        default_factory=list, metadata={"name": "SAMPLE"}
    )


config = ParserConfig(
    fail_on_unknown_properties=False,
    fail_on_unknown_attributes=False,
)


def get_checklist_metadata(sample: str) -> List[SampleAttribute]:
    logging.info(
        f"Fetching checklist metadata from ENA {API_ROOT = } for sample {sample}"
    )
    response = requests.get(f"{API_ROOT}/xml/{sample}", auth=ENA_AUTH)
    if response.status_code != requests.codes.ok:
        logging.info(
            f"No metadata available for {sample}. Status code {response.status_code}"
        )
        return []
    metadata = XmlParser(config=config).from_string(response.text, SampleMetadataSet)
    if not metadata.samples:
        logging.info(f"No sample in metadata of {sample}")
        return []
    return metadata.samples[0].attributes.values
