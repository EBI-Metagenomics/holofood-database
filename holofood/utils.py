import logging
import time
from datetime import timedelta
from typing import Any

from django.conf import settings
from django.db.models import Aggregate, Func

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


class CadenceEnforcer:
    def __init__(self, min_period: timedelta = timedelta(0)):
        """
        Ensures that at least min_period time has passed between invocations.
        :param min_period: Any timedelta e.g. datetime.timedelta(seconds=3)
        """
        self.cadence_seconds = min_period.total_seconds()
        self.prev_return = None

    def __call__(self):
        now = time.time()
        if self.prev_return:
            since = now - self.prev_return
            if since < self.cadence_seconds:
                logging.debug(f"Sleeping for {self.cadence_seconds - since:.2f}s")
                time.sleep(self.cadence_seconds - since)
        self.prev_return = now
        return


class StringAgg(Aggregate):
    dbengine = settings.DATABASES["default"]["ENGINE"].lower()
    if "postgres" in dbengine:
        function = "STRING_AGG"
        template = "%(function)s(%(distinct)s%(expressions)s, ',')"
    elif "sqlite" in dbengine:
        function = "GROUP_CONCAT"
    else:
        function = "MIN"
    name = "Concat"


class DistinctFunc(Func):
    template = "%(function)s(DISTINCT %(expressions)s)"
