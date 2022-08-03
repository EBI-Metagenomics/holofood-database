from typing import Any

from django.conf import settings

from holofood.config import HolofoodConfig

holofood_config: HolofoodConfig = settings.HOLOFOOD_CONFIG


def clean_keys(data: Any) -> Any:
    """
    Clean keys of a dictionary to be valid python variable names, by replacing spaces and hyphens with underscores.
    :param data: Dictionary (or list with potentially dicts inside) to clean, e.g. {'attributes': {'some-thing': [1, 2]}}
    :return: Data with dict keys cleaned, e.g. {'attributes': {'some_thing': [1, 2]}}
    """
    if isinstance(data, list):
        return list(map(clean_keys, data))
    elif isinstance(data, dict):
        return {
            k.replace(" ", "_").replace("-", "_"): clean_keys(v)
            for k, v in data.items()
        }
    return data
