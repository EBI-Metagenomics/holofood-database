from django.conf import settings  # import the settings file


def apis(request):
    return {"ENA_BROWSER_URL": settings.HOLOFOOD_CONFIG.ena.browser_url}
