from django.conf import settings
from requests.auth import HTTPBasicAuth


ENA_AUTH = HTTPBasicAuth(
    settings.HOLOFOOD_CONFIG.ena.username, settings.HOLOFOOD_CONFIG.ena.password
)
