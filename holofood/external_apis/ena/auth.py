from requests.auth import HTTPBasicAuth

from holofood.utils import holofood_config

if holofood_config.ena.username:
    ENA_AUTH = HTTPBasicAuth(holofood_config.ena.username, holofood_config.ena.password)
else:
    ENA_AUTH = None
