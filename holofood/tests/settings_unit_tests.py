from holofood.settings import *

UNIT_TESTING = True

HOLOFOOD_CONFIG = HolofoodConfig(
    _env_file=holofood_config_env,
)

del STORAGES  # disable whitenoise static file serving
