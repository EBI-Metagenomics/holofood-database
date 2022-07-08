from holofood.utils import holofood_config


def apis(request):
    return {
        "ENA_BROWSER_URL": holofood_config.ena.browser_url,
        "MGNIFY_WEB_URL": holofood_config.mgnify.web_url,
    }
